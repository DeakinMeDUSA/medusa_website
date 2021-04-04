from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, FormView, ListView, TemplateView
from rest_framework import generics
from rest_framework.request import Request

from medusa_website.mcq_bank.models import (
    Answer,
    Category,
    Progress,
    Question,
    Quiz,
    Record,
    Sitting,
)

from ..users.admin import User
from .exceptions import AnswerRecordNotValid, UserNotValid
from .forms import QuestionForm
from .models.quiz_session import QuizSession
from .serializers import AnswerSerializer, QuestionSerializer, RecordSerializer


class QuestionListCreate(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_url_kwarg = "id"


class AnswerRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    lookup_url_kwarg = "id"


class AnswersList(generics.ListAPIView):
    serializer_class = AnswerSerializer

    def get_queryset(self):
        queryset = Answer.objects.all()
        question_id = self.request.query_params.get("question_id", None)
        if question_id is not None:
            queryset = queryset.filter(question_id=question_id)
        return queryset


class RecordHistory(generics.ListAPIView):
    serializer_class = RecordSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Record.objects.filter(user=user)
        question_id = self.request.query_params.get("question_id", None)
        if question_id is not None:
            queryset = queryset.filter(question__id=question_id)
        return queryset


class RecordCreate(generics.CreateAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

    def create(self, request: Request, *args, **kwargs):
        print(f"request.data = {request.data}")
        user_id = request.data.get("user")
        question = request.data.get("question")
        answer = request.data.get("answer")
        if question is None or answer is None:
            raise AnswerRecordNotValid()

        try:
            User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise UserNotValid(f"Could not find user for user id = {user_id}")

        request.data["timestamp"] = timezone.now()

        return super().create(request, *args, **kwargs)


class AnswerCreate(generics.CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class QuizIndex(TemplateView):
    template_name = "mcq_bank/index.html"


class QuizMarkerMixin(object):
    @method_decorator(login_required)
    @method_decorator(permission_required("quiz.view_sittings"))
    def dispatch(self, *args, **kwargs):
        return super(QuizMarkerMixin, self).dispatch(*args, **kwargs)


class SittingFilterTitleMixin(object):
    def get_queryset(self):
        queryset = super(SittingFilterTitleMixin, self).get_queryset()
        quiz_filter = self.request.GET.get("quiz_filter")
        if quiz_filter:
            queryset = queryset.filter(quiz__title__icontains=quiz_filter)

        return queryset


class QuizListView(ListView):
    template_name = "mcq_bank/quiz_list.html"

    queryset = Quiz.objects.filter(draft=False)
    # def get_queryset(self):
    #     queryset = super(QuizListView, self).get_queryset()
    #     return queryset.filter(draft=False)


class QuizDetailView(DetailView):
    model = Quiz

    template_name = "mcq_bank/quiz_detail.html"

    def get(self, request, *args, **kwargs):
        self.quiz = get_object_or_404(Quiz, url=self.kwargs["quiz_name"])

        self.object = self.quiz
        if self.object.draft and not request.user.has_perm("quiz.change_quiz"):
            raise PermissionDenied

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class CategoriesListView(ListView):
    model = Category
    template_name = "mcq_bank/category_list.html"


class ViewQuizListByCategory(ListView):
    model = Quiz
    template_name = "mcq_bank/view_quiz_category.html"

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(
            Category, category=self.kwargs["category_name"]
        )

        return super(ViewQuizListByCategory, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ViewQuizListByCategory, self).get_context_data(**kwargs)

        context["category"] = self.category
        return context

    def get_queryset(self):
        queryset = super(ViewQuizListByCategory, self).get_queryset()
        return queryset.filter(category=self.category, draft=False)


class QuizUserProgressView(TemplateView):
    template_name = "mcq_bank/progress.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(QuizUserProgressView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(QuizUserProgressView, self).get_context_data(**kwargs)
        progress, c = Progress.objects.get_or_create(user=self.request.user)
        context["cat_scores"] = progress.list_all_cat_scores
        context["exams"] = progress.show_exams()
        return context


class QuizMarkingList(QuizMarkerMixin, SittingFilterTitleMixin, ListView):
    model = Sitting

    def get_queryset(self):
        queryset = super(QuizMarkingList, self).get_queryset().filter(complete=True)

        user_filter = self.request.GET.get("user_filter")
        if user_filter:
            queryset = queryset.filter(user__username__icontains=user_filter)

        return queryset


class QuizMarkingDetail(QuizMarkerMixin, DetailView):
    model = Sitting

    def post(self, request, *args, **kwargs):
        sitting: Sitting = self.get_object()

        q_to_toggle = request.POST.get("qid", None)
        if q_to_toggle:
            q = Question.objects.get(id=int(q_to_toggle))
            if int(q_to_toggle) in sitting.get_incorrect_questions:
                sitting.remove_incorrect_question(q)
            else:
                sitting.add_incorrect_question(q)

        return self.get(request)

    def get_context_data(self, **kwargs):
        context = super(QuizMarkingDetail, self).get_context_data(**kwargs)
        context["questions"] = context["sitting"].get_questions(with_answers=True)
        return context


class QuizTake(FormView):
    form_class = QuestionForm
    template_name = "mcq_bank/question.html"
    result_template_name = "mcq_bank/result.html"
    single_complete_template_name = "mcq_bank/single_complete.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.quiz = get_object_or_404(Quiz, url=self.kwargs["quiz_name"])
        if self.quiz.draft and not request.user.has_perm("quiz.change_quiz"):
            raise PermissionDenied

        self.logged_in_user = self.request.user.is_authenticated
        self.sitting = Sitting.objects.user_sitting(request.user, self.quiz)
        if self.sitting is False:
            return render(request, self.single_complete_template_name)

        return super(QuizTake, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):

        self.question = self.sitting.get_first_question()
        self.progress = self.sitting.progress()

        form_class = self.form_class

        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        kwargs = super(QuizTake, self).get_form_kwargs()

        return dict(kwargs, question=self.question)

    def form_valid(self, form):

        self.form_valid_user(form)
        if self.sitting.get_first_question() is False:
            return self.final_result_user()

        self.request.POST = {}

        return super(QuizTake, self).get(self, self.request)

    def get_context_data(self, **kwargs):
        context = super(QuizTake, self).get_context_data(**kwargs)
        context["question"] = self.question
        context["quiz"] = self.quiz
        if hasattr(self, "previous"):
            context["previous"] = self.previous
        if hasattr(self, "progress"):
            context["progress"] = self.progress
        return context

    def form_valid_user(self, form):
        progress, c = Progress.objects.get_or_create(user=self.request.user)
        guess = form.cleaned_data["answers"]
        is_correct = self.question.check_if_correct(guess)

        if is_correct is True:
            self.sitting.add_to_score(1)
            progress.update_score(self.question, 1, 1)
        else:
            self.sitting.add_incorrect_question(self.question)
            progress.update_score(self.question, 0, 1)

        if self.quiz.answers_at_end is not True:
            self.previous = {
                "previous_answer": guess,
                "previous_outcome": is_correct,
                "previous_question": self.question,
                "answers": self.question.get_answers(),
            }
        else:
            self.previous = {}

        self.sitting.add_user_answer(self.question, guess)
        self.sitting.remove_first_question()

    def final_result_user(self):
        results = {
            "quiz": self.quiz,
            "score": self.sitting.get_current_score,
            "max_score": self.sitting.get_max_score,
            "percent": self.sitting.get_percent_correct,
            "sitting": self.sitting,
            "previous": self.previous,
        }

        self.sitting.mark_quiz_complete()

        if self.quiz.answers_at_end:
            results["questions"] = self.sitting.get_questions(with_answers=True)
            results["incorrect_questions"] = self.sitting.get_incorrect_questions

        if self.quiz.exam_paper is False:
            self.sitting.delete()

        return render(self.request, self.result_template_name, results)
