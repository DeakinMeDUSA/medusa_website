from bootstrap_modal_forms.generic import BSModalFormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from vanilla import CreateView, DetailView, ListView

from medusa_website.mcq_bank.forms import (
    QuizSessionContinueOrStopForm,
    QuizSessionCreateForm,
    QuizSessionCreateFromQuestionsForm,
)
from medusa_website.mcq_bank.models import QuizSession


class QuizSessionListView(LoginRequiredMixin, ListView):
    model = QuizSession
    template_name = "mcq_bank/session_history.html"
    context_object_name = "quiz_sessions"


class QuizSessionDetailView(LoginRequiredMixin, DetailView):
    model = QuizSession
    template_name = "mcq_bank/quiz_session_detail.html"
    context_object_name = "quiz_session"
    lookup_field = "id"

    def get_context_data(self, **kwargs):
        context = super(QuizSessionDetailView, self).get_context_data(**kwargs)
        context["is_current"] = context["quiz_session"].is_current
        context["questions"] = context["quiz_session"].questions.all()
        context["answers"] = context["quiz_session"].answers.all()
        print(context)
        return context


@login_required
def complete_session(request, **kwargs):
    # Simple endpoint to mark a quiz session as complete when a button is pressed
    quiz_session = QuizSession.objects.get(id=kwargs["id"])
    quiz_session.mark_quiz_complete()
    return HttpResponseRedirect(reverse("mcq_bank:quiz_session_detail", kwargs={"id": quiz_session.id}))


class QuizSessionEndOrContinueView(LoginRequiredMixin, BSModalFormView):
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
        context = self.get_context_data()
        if context.get("current_session"):
            return self.render_to_response(context)
        else:
            return HttpResponseRedirect(reverse("mcq_bank:quiz_session_create"))

    def get_context_data(self, *args, **kwargs):
        context = super(QuizSessionEndOrContinueView, self).get_context_data(**kwargs)
        current_session = QuizSession.get_current(user=self.user)
        progress = current_session.progress if current_session else (0, 0)
        context["current_session"] = current_session
        context["questions_answered"] = progress[0]
        context["questions_total"] = progress[1]
        context["percent_complete"] = round(100 * progress[0] / progress[1], 2) if progress[1] > 0 else 0

        return context

    def form_valid(self, form):
        # We don't care about the form data
        return True

    def post(self, request, *args, **kwargs):
        current_session = QuizSession.get_current(user=self.request.user)
        if request.POST["choice"] == "start_over":
            print("Finishing current session and creating new one")
            try:
                current_session.mark_quiz_complete()
            except AttributeError:
                pass
            return HttpResponseRedirect(reverse("mcq_bank:quiz_session_create"))

        elif request.POST["choice"] == "continue":
            return HttpResponseRedirect(reverse("mcq_bank:run_session"))

        else:
            raise RuntimeError(f"Form choice {request.POST['choice']} is invalid!")


class QuizSessionCreateFromQuestionsView(LoginRequiredMixin, CreateView):
    model = QuizSession
    template_name = "mcq_bank/quiz_session_create.html"
    context_object_name = "quiz_session"
    lookup_field = "id"
    form_class = QuizSessionCreateFromQuestionsForm

    def post(self, request, *args, **kwargs):
        form = self.get_form(data=request.POST, files=request.FILES)
        if form.is_valid():
            current_session = QuizSession.get_current(user=form.cleaned_data["user"])
            if current_session:
                current_session.mark_quiz_complete()
            new_session = QuizSession.create_from_questions(
                user=form.cleaned_data["user"],
                questions=form.cleaned_data["questions"],
                max_n=10000,
                randomise_order=True,
                include_answered=True,
                save=True,
            )
            return HttpResponseRedirect(reverse("mcq_bank:run_session"))
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(QuizSessionCreateFromQuestionsView, self).get_context_data(**kwargs)
        return context


class QuizSessionCreateView(LoginRequiredMixin, CreateView):
    model = QuizSession
    template_name = "mcq_bank/quiz_session_create.html"
    context_object_name = "quiz_session"
    lookup_field = "id"
    form_class = QuizSessionCreateForm

    # def get_form(self, data=None, files=None, **kwargs):
    #     user = self.request.user
    #     return QuizSessionCreateForm(data, files, user=user, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(QuizSessionCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = self.get_form(data=request.POST, files=request.FILES)
        if QuizSession.get_current(user=request.user) is not None:
            form.add_error("There is a current session already in pregress!")
            return self.form_invalid(form)
        elif form.is_valid():
            quiz_session = QuizSession.create_from_categories(
                user=self.request.user,
                categories=form.cleaned_data["categories"],
                max_n=int(form.cleaned_data["max_num_questions"]),
                randomise_order=form.cleaned_data["randomise_order"],
                include_answered=form.cleaned_data["include_answered"],
            )
            return HttpResponseRedirect(reverse("mcq_bank:run_session"))
        else:
            return self.form_invalid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(QuizSessionCreateView, self).get_context_data(**kwargs)
        context["has_current_session"] = True if QuizSession.get_current(user=self.request.user) is not None else False
        return context
