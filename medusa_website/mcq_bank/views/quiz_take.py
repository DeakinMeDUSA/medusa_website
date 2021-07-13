from typing import Optional

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import FormView

from medusa_website.mcq_bank.models import Answer, History, Question, QuizSession

from ...users.models import User
from ..forms import QuestionForm


class QuizTakeView(FormView, LoginRequiredMixin):
    form_class = QuestionForm
    template_name = "mcq_bank/question.html"
    result_template_name = "mcq_bank/result.html"
    session_create_template_name = "mcq_bank/quiz_session_create.html"
    single_complete_template_name = "mcq_bank/single_complete.html"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user: Optional[User] = None
        self.session: Optional[QuizSession] = None
        self.question: Optional[Question] = None
        self.history: Optional[History] = None

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = self.request.user
        print(f"User = {self.user}")
        self.session = QuizSession.get_current(request.user)
        print(f"Session = {self.session}")
        if self.session is None:
            return redirect("mcq_bank:quiz_session_create")
        self.history = self.user.history

        return super(QuizTakeView, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):

        self.question = self.session.current_question
        self.history = self.session.progress

        form_class = self.form_class

        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        kwargs = super(QuizTakeView, self).get_form_kwargs()

        return dict(kwargs, question=self.question)

    def form_valid(self, form):

        self.form_valid_user(form)
        if self.session.remaining_questions.count() == 0:
            return self.final_result_user()

        self.request.POST = {}

        return super(QuizTakeView, self).get(self, self.request)

    def get_context_data(self, **kwargs):
        context = super(QuizTakeView, self).get_context_data(**kwargs)
        context["question"] = self.question
        context["session"] = self.session
        if hasattr(self, "previous"):
            context["previous"] = self.previous
        if hasattr(self, "progress"):
            context["progress"] = self.history
        return context

    def form_valid_user(self, form):
        answer = Answer.objects.get(id=form.cleaned_data["answers"])
        self.session.add_user_answer(answer=answer)

        self.previous = {
            "previous_answer": answer,
            "previous_outcome": answer.correct,
            "previous_question": self.question,
            "answers": self.question.get_answers(),
        }

    def final_result_user(self):
        results = {
            "session": self.session,
            "score": self.session.correct_answers.count(),
            "max_score": self.session.questions.count(),
            "percent": self.session.percent_correct,
            "previous": self.previous,
        }

        self.session.mark_quiz_complete()

        return render(self.request, self.result_template_name, results)
