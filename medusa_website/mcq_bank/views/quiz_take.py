from typing import Optional

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template import loader
from django.views.generic import FormView
from vanilla import DetailView

from medusa_website.mcq_bank.models import Answer, History, Question, QuizSession

from ...users.models import User
from ..forms import QuestionForm


class QuizTakeView(LoginRequiredMixin, FormView, DetailView):
    form_class = QuestionForm
    template_name = "mcq_bank/question.html"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user: Optional[User] = None
        self.session: Optional[QuizSession] = None
        self.question: Optional[Question] = None
        self.history: Optional[History] = None

    def dispatch(self, request, *args, **kwargs):
        self.user = self.request.user
        self.session = QuizSession.get_current(request.user)
        if self.session is None:
            return redirect("mcq_bank:quiz_session_create")
        self.history = self.user.history

        # Set question index to match url if specified
        if self.request.GET.get("q"):
            question_index = int(self.request.GET["q"])
            if question_index < 0 or question_index > self.session.questions.count() - 1:
                raise ValueError("Invalid question index specified!")
            else:
                self.session.current_question_index = question_index

            self.session.save()

        return super(QuizTakeView, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):

        self.question = self.session.current_question
        self.history = self.session.progress

        form_class = self.form_class

        return form_class(question=self.question, **self.get_form_kwargs())

    # def get_form_kwargs(self):
    #     kwargs = super(QuizTakeView, self).get_form_kwargs()
    #
    #     return dict(kwargs, question=self.question)

    def form_valid(self, form):
        submitted_answer = self.submit_answer_response(form)

        answer_response = self.render_answer_response(request=self.request, submitted_answer=submitted_answer)
        return JsonResponse({"answer_response": answer_response})

    def get_context_data(self, **kwargs):
        context = super(QuizTakeView, self).get_context_data(**kwargs)
        context["question"] = self.question
        context["session"] = self.session
        if self.session.current_question_response is not None:
            context["submitted_answer"] = self.session.current_question_response

        return context

    def submit_answer_response(self, form) -> Answer:
        submitted_answer = Answer.objects.get(id=form.cleaned_data["answers"])
        self.session.add_user_answer(answer=submitted_answer)
        return submitted_answer

    def render_answer_response(self, request, submitted_answer) -> str:
        context = {
            "submitted_answer": submitted_answer,
            "question": submitted_answer.question,
        }
        return loader.render_to_string("mcq_bank/answer_response.html", context=context, request=request)


class QuestionPreviewView(LoginRequiredMixin, FormView, DetailView):
    """Preview a MCQ question  in the same template as during a quiz"""

    lookup_field = "id"
    model = Question
    form_class = QuestionForm
    template_name = "mcq_bank/question.html"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user: Optional[User] = None
        self.object: Optional[Question] = None
        self.question: Optional[Question] = None

    def dispatch(self, request, *args, **kwargs):
        self.user = self.request.user
        self.object = self.get_object()
        self.question = self.object
        return super(QuestionPreviewView, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        assert self.question is not None
        form_class = self.form_class

        return form_class(question=self.question, **self.get_form_kwargs())

    # def get_form_kwargs(self):
    #     kwargs = super(QuizTakeView, self).get_form_kwargs()
    #
    #     return dict(kwargs, question=self.question)

    def form_valid(self, form):
        answer_response = self.render_answer_response(
            request=self.request, submitted_answer=self.get_submitted_answer()
        )
        return JsonResponse({"answer_response": answer_response})

    def get_submitted_answer(self) -> Answer:
        # Provide an example answer to show response
        return self.question.correct_answers[0]

    def get_context_data(self, **kwargs):
        context = super(QuestionPreviewView, self).get_context_data(**kwargs)
        context["question"] = self.question
        context["submitted_answer"] = self.get_submitted_answer()
        context["answer_response"] = self.render_answer_response(
            self.request, submitted_answer=self.get_submitted_answer()
        )

        return context

    def render_answer_response(self, request, submitted_answer) -> str:
        context = {
            "submitted_answer": submitted_answer,
            "question": submitted_answer.question,
        }
        return loader.render_to_string("mcq_bank/answer_response.html", context=context, request=request)
