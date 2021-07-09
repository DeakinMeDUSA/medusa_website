from bootstrap_modal_forms.generic import BSModalFormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from vanilla import CreateView, DetailView, ListView

from medusa_website.mcq_bank.forms import (
    QuizSessionContinueOrStopForm,
    QuizSessionCreateForm,
)
from medusa_website.mcq_bank.models import QuizSession


class QuizSessionListView(ListView, LoginRequiredMixin):
    model = QuizSession
    template_name = "mcq_bank/session_history.html"
    context_object_name = "quiz_sessions"


class QuizSessionDetailView(DetailView):
    model = QuizSession
    template_name = "mcq_bank/quiz_session_detail.html"
    context_object_name = "quiz_session"
    lookup_field = "id"

    def get_context_data(self, **kwargs):
        context = super(QuizSessionDetailView, self).get_context_data(**kwargs)
        context["questions"] = context["quiz_session"].questions.all()
        context["answers"] = context["quiz_session"].answers.all()
        print(context)
        return context


class QuizSessionEndOrContinueView(BSModalFormView, LoginRequiredMixin):
    template_name = "mcq_bank/session_end_or_continue_modal.html"
    form_class = QuizSessionContinueOrStopForm

    # def get(self, request, *args, **kwargs):
    #     self.user = request.user
    #     self.session = QuizSession.get_current(user=self.user)
    #     print(f"self.user = {self.user}")
    #     return super(QuizSessionEndOrContinueView, self).get(*args, **kwargs)

    def get_object(self, queryset=None):
        return QuizSession.get_current(user=self.user)

    def get(self, request, *args, **kwargs):
        self.user = self.request.user
        return super(QuizSessionEndOrContinueView, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(QuizSessionEndOrContinueView, self).get_context_data(**kwargs)
        current_session = QuizSession.get_current(user=self.user)
        progress = current_session.progress if current_session else (0, 0)
        context["questions_answered"] = progress[0]
        context["questions_total"] = progress[1]
        context["percent_complete"] = round(100 * progress[0] / progress[1], 2) if progress[1] > 0 else 0

        print(context)
        return context

    def form_valid(self, form):
        # We don't care about the form data
        return True

    def post(self, request, *args, **kwargs):
        current_session = QuizSession.get_current(user=self.request.user)
        if request.POST["choice"] == "start_over":
            print("Finishing current session and creating new one")
            current_session.mark_quiz_complete()
            return HttpResponseRedirect(reverse("mcq_bank:quiz_session_create"))

        elif request.POST["choice"] == "continue":
            return HttpResponseRedirect(reverse("mcq_bank:run_session"))

        else:
            raise RuntimeError(f"Form choice {request.POST['choice']} is invalid!")


class QuizSessionCreateView(CreateView, LoginRequiredMixin):
    model = QuizSession
    template_name = "mcq_bank/quiz_session_create.html"
    context_object_name = "quiz_session"
    lookup_field = "id"
    form_class = QuizSessionCreateForm

    # def get_form(self, data=None, files=None, **kwargs):
    #     user = self.request.user
    #     return QuizSessionCreateForm(data, files, user=user, **kwargs)

    def get(self, request, *args, **kwargs):
        self.user = request.user
        self.session = QuizSession.get_current(user=self.user)
        print(f"self.user = {self.user}")
        return super(QuizSessionCreateView, self).get(request, *args, **kwargs)

    def get_form_class(self):
        if self.session is not None:
            return QuizSessionContinueOrStopForm
        else:
            return QuizSessionCreateForm

    def post(self, request, *args, **kwargs):
        self.session = QuizSession.get_current(user=request.user)
        form = self.get_form_class()(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            user = request.user
            max_questions = int(form.cleaned_data["max_num_questions"])
            categories = form.cleaned_data["categories"]
            include_answered = form.cleaned_data["include_answered"]
            randomise_order = form.cleaned_data["randomise_order"]
            quiz_session = QuizSession.create_from_categories(
                user=user,
                categories=categories,
                max_n=max_questions,
                include_answered=include_answered,
                randomise_order=randomise_order,
            )

            # return HttpResponseRedirect(reverse("mcq_bank:quiz_session_run", kwargs={"id": quiz_session.id}))
            return HttpResponseRedirect(reverse("mcq_bank:quiz_session_detail", kwargs={"id": quiz_session.id}))

    def get_context_data(self, *args, **kwargs):
        context = super(QuizSessionCreateView, self).get_context_data(**kwargs)
        context["current_session"] = QuizSession.get_current(user=self.user)
        print(context)
        return context


class QuizSessionRunView(DetailView):
    model = QuizSession
    template_name = "mcq_bank/quiz_session_run.html"
    context_object_name = "quiz_session"
    lookup_field = "id"

    # form_class = QuizSessionCreateForm

    def get_context_data(self, **kwargs):
        context = super(QuizSessionRunView, self).get_context_data(**kwargs)
        context["questions"] = context["quiz_session"].questions.all()
        context["answers"] = context["quiz_session"].answers.all()
        print(context)
        return context


#
# class QuizSessionView(FormView):
#     form_class = QuestionForm
#     template_name = "mcq_bank/question.html"
#     result_template_name = "mcq_bank/result.html"
#     single_complete_template_name = "mcq_bank/single_complete.html"
#
#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         self.quiz_session = QuizSession.objects.get_current_session(user=User)
#         if self.quiz_session is None:
#             return render(request, self.single_complete_template_name)
#
#         return super(QuizSessionView, self).dispatch(request, *args, **kwargs)
#
#     def get_form(self, *args, **kwargs):
#
#         self.question = self.quiz_session.current_question
#         self.progress = self.quiz_session.progress
#
#         form_class = self.form_class
#
#         return form_class(**self.get_form_kwargs())
#
#     def get_form_kwargs(self):
#         kwargs = super(QuizSessionView, self).get_form_kwargs()
#
#         return dict(kwargs, question=self.question)
#
#     def form_valid(self, form):
#
#         self.form_valid_user(form)
#         if self.quiz_session.remaining_questions.count() == 0:
#             return self.final_result_user()
#
#         self.request.POST = {}
#
#         return super(QuizSessionView, self).get(self, self.request)
#
#     def get_context_data(self, **kwargs):
#         context = super(QuizSessionView, self).get_context_data(**kwargs)
#         context["question"] = self.question
#         context["quiz_session"] = self.quiz_session
#         if hasattr(self, "previous"):
#             context["previous"] = self.previous
#         if hasattr(self, "progress"):
#             context["progress"] = self.progress
#         return context
#
#     def form_valid_user(self, form):
#         # progress, c = History.objects.get_or_create(user=self.request.user)
#         guess = form.cleaned_data["answers"]
#         answer = Answer.objects.get(id=guess)
#
#         # if self.quiz.answers_at_end is not True:
#         self.previous = {
#             "previous_answer": answer,
#             "previous_outcome": answer.correct,
#             "previous_question": self.question,
#             "answers": self.question.get_answers(),
#         }
#         # else:
#         #     self.previous = {}
#
#         self.quiz_session.add_user_answer(answer=answer)
#
#     def final_result_user(self):
#         results = {
#             "quiz_session": self.quiz_session,
#             "score": self.quiz_session.get_current_score,
#             "max_score": self.quiz_session.get_max_score,
#             "percent": self.quiz_session.get_percent_correct,
#             "previous": self.previous,
#         }
#
#         self.sitting.mark_quiz_complete()
#
#         if self.quiz.answers_at_end:
#             results["questions"] = self.sitting.get_questions(with_answers=True)
#             results["incorrect_questions"] = self.sitting.get_incorrect_questions
#
#         if self.quiz.exam_paper is False:
#             self.sitting.delete()
#
#         return render(self.request, self.result_template_name, results)
