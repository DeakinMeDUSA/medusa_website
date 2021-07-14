import logging
from typing import Optional, Tuple, List

import django_tables2 as tables
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet
from django.forms import Form
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.html import format_html
from django_filters import FilterSet
from django_filters.views import FilterView
from vanilla import ListView, UpdateView, CreateView, DetailView

from medusa_website.mcq_bank.forms import (
    QuestionCreateForm,
    QuestionDetailForm,
    QuestionUpdateForm,
    AnswerFormSetHelper,
    AnswerCreateFormSet,
    AnswerUpdateFormSet,
    AnswerDetailFormSet,
    QuizSessionCreateFromQuestionsForm,
)
from medusa_website.mcq_bank.models import Question
from medusa_website.users.models import User

logger = logging.getLogger(__name__)


# TODO fix Question_create javascript to add answers again


def validate_answer_formset(answer_formset: AnswerCreateFormSet) -> Tuple[bool, AnswerCreateFormSet, List[Form]]:
    # Check at least two answers provided
    complete_answer_forms = []
    incomplete_answer_forms = []
    invalid_answer_forms = []
    answer_forms = [ansform for ansform in answer_formset.forms if ansform not in answer_formset.deleted_forms]
    for answer_form in answer_forms:
        if answer_form.is_valid():
            if answer_form.instance.text and len(answer_form.instance.text) > 0:
                complete_answer_forms.append(answer_form)
            else:
                incomplete_answer_forms.append(answer_form)
        else:
            invalid_answer_forms.append(answer_form)
    answer_texts = set([ansform.instance.text for ansform in complete_answer_forms])

    if len(invalid_answer_forms) > 0:
        return False, answer_formset, complete_answer_forms
    elif len(complete_answer_forms) < 2:
        for answer_form in incomplete_answer_forms:
            answer_form.add_error(field="text", error="Two or more answers must be specified")
        return False, answer_formset, complete_answer_forms
    elif len(complete_answer_forms) > 10:
        for answer_form in complete_answer_forms[9:]:
            answer_form.add_error(field="text", error="A maximum of 10 answers can be specified")
        return False, answer_formset, complete_answer_forms
    elif len([ansform for ansform in complete_answer_forms if ansform.instance.correct]) != 1:
        for answer_form in complete_answer_forms:
            answer_form.add_error(field="text", error="There must be exactly one correct answer specified")
        return False, answer_formset, complete_answer_forms
    elif len(answer_texts) != len(complete_answer_forms):
        for answer_form in complete_answer_forms:
            answer_form.add_error(field="text", error="All answers must be unique for a particular question!")
        return False, answer_formset, complete_answer_forms
    else:
        return True, answer_formset, complete_answer_forms


def editable(user: User, question: Question):
    return user.is_staff or question.author == user


class QuestionDetailView(LoginRequiredMixin, DetailView):
    model = Question
    template_name = "mcq_bank/question_detail.html"
    form_class = QuestionDetailForm
    context_object_name = "question"
    lookup_field = "id"
    queryset = Question.objects.all()

    #
    def get(self, request, *args, **kwargs):

        self.object = self.get_object()
        form = self.get_form(instance=self.object)

        author_change_permission = request.user.is_staff or request.user.is_superuser
        if author_change_permission is False:
            form.fields["author"].disabled = True

        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        """
        Returns the object the view is displaying.
        """
        question = Question.objects.get(id=self.kwargs["id"])
        self.object = question
        return question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["question"].refresh_from_db()
        context["editable"] = editable(self.request.user, question=context["question"])
        context["answer_formset_helper"] = AnswerFormSetHelper()
        if context.get("answer_formset") is None:
            context["answer_formset"] = kwargs.get("answer_formset") or AnswerDetailFormSet(
                instance=context["question"]
            )

        return context


class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    template_name = "mcq_bank/question_update.html"
    form_class = QuestionUpdateForm
    context_object_name = "question"
    lookup_field = "id"
    queryset = Question.objects.all()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(instance=self.object)

        author_change_permission = request.user.is_staff or request.user.is_superuser
        if author_change_permission is False:
            form.fields["author"].disabled = True

        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        question_old = self.get_object()
        self.object = question_old
        orig_author = question_old.author
        form = self.get_form(
            data=request.POST,
            files=request.FILES,
            instance=question_old,
        )
        if form.is_valid():
            updated_question: Question = form.save(commit=False)
            updated_question.author = form.instance.author or orig_author
        else:
            return self.form_invalid(form)

        # parent_model, request, instance, view_kwargs = None, view = None
        answer_formset = AnswerUpdateFormSet(
            data=self.request.POST, files=self.request.FILES, instance=updated_question
        )

        return self.formset_valid(form, answer_formset)

    def get_object(self, queryset=None):
        """
        Returns the object the view is displaying.
        """
        queryset = self.get_queryset()
        lookup_url_kwarg = self.lookup_field

        try:
            lookup = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        except KeyError:
            msg = "Lookup field '%s' was not provided in view kwargs to '%s'"
            raise ImproperlyConfigured(msg % (lookup_url_kwarg, self.__class__.__name__))

        return get_object_or_404(queryset, **lookup)

    def get_template_names(self):
        if editable(self.request.user, self.get_object()):
            self.template_name = "mcq_bank/question_update.html"
        else:
            self.template_name = "mcq_bank/question_detail.html"
        return super(QuestionUpdateView, self).get_template_names()

    def get_form_class(self):
        if self.request.method == "GET" and editable(self.request.user, self.get_object()) is False:
            return QuestionDetailForm
        else:
            return QuestionUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["editable"] = editable(self.request.user, question=self.get_object())
        context["question"] = context.get("question") or self.get_object()

        context["answer_formset_helper"] = AnswerFormSetHelper()
        if context.get("answer_formset") is None:
            if self.request.POST:
                context["answer_formset"] = AnswerUpdateFormSet(
                    data=self.request.POST, instance=context["question"], files=self.request.FILES
                )
                # queryset=context["question"].answers.all())
            else:
                context["answer_formset"] = AnswerUpdateFormSet(
                    instance=context["question"], queryset=context["question"].answers.all()
                )
        return context

    def fix_missing_author(self, form):
        if isinstance(form.cleaned_data["author"], User) is False:
            print(f"Author came in as {form.cleaned_data['author']}, resetting to prior value: {form.instance.user}")
            form.cleaned_data["author"] = form.instance.author
        return super().form_valid(form)

    def formset_valid(self, form, answer_formset):
        is_valid, answer_formset_with_errors, complete_answer_forms = validate_answer_formset(answer_formset)
        if is_valid is False:
            return self.render_to_response(self.get_context_data(form=form, answer_formset=answer_formset_with_errors))

        for to_delete in answer_formset.deleted_forms:
            logger.info(f"Deleting model: {to_delete.instance}")
            to_delete.instance.delete()
        form.save()
        for ansforms in complete_answer_forms:
            ansforms.save()
        self.object = form.instance
        return HttpResponseRedirect(self.get_success_url())


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question

    # fields = ["text", "category", "image", "explanation", "randomise_answer_order"]
    template_name = "mcq_bank/question_create.html"
    form_class = QuestionCreateForm
    lookup_field = "id"

    def post(self, request, *args, **kwargs):
        form = self.get_form(
            data=request.POST,
            files=request.FILES,
        )
        if form.is_valid():
            new_question: Question = form.save(commit=False)
        else:
            return self.form_invalid(form)

        # parent_model, request, instance, view_kwargs = None, view = None
        answer_formset = AnswerCreateFormSet(data=self.request.POST, files=self.request.FILES, instance=new_question)

        return self.formset_valid(form, answer_formset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["question"] = kwargs["form"].instance
            context["answer_formset"] = kwargs.get("answer_formset") or AnswerCreateFormSet(
                instance=context["question"]
            )
        else:
            context["answer_formset"] = AnswerCreateFormSet()

        context["answer_formset_helper"] = AnswerFormSetHelper()

        return context

    def formset_valid(self, form: QuestionCreateForm, answer_formset):
        is_valid, answer_formset_with_errors, complete_answer_forms = validate_answer_formset(answer_formset)
        if is_valid is False:
            return self.render_to_response(self.get_context_data(form=form, answer_formset=answer_formset_with_errors))

        question = form.save(commit=False)
        question.author = self.request.user
        question.save()
        for ansforms in complete_answer_forms:
            ansforms.save()
        return HttpResponseRedirect(question.get_absolute_url())


class QuestionListFilter(FilterSet):
    class Meta:
        model = Question
        fields = ["category", "author"]


class QuestionListTable(tables.Table):
    class Meta:
        attrs = {
            "class": "table tablesorter-metro-dark",  # Sorting is handled by js to avoid refresh
            "id": "question-list-table",
        }
        model = Question
        exclude = ("randomise_answer_order", "flagged_by", "is_reviewed", "reviewed_by")
        sequence = ("id", "author", "category", "answered", "text", "answer", "explanation", "image")

    id = tables.Column(linkify=False, accessor="id", orderable=False)
    author = tables.Column(linkify=True, orderable=False)
    category = tables.Column(linkify=True, orderable=False)
    answered = tables.Column(linkify=False, orderable=False, empty_values=())
    text = tables.Column(linkify=False, orderable=False)
    answer = tables.Column(linkify=False, orderable=False, empty_values=(), verbose_name="Answer")
    explanation = tables.Column(linkify=False, orderable=False)
    image = tables.Column(linkify=False, orderable=False)
    is_flagged = tables.Column(linkify=False, orderable=False)
    filterset_class = QuestionListFilter

    # def __init__(self, *args, **kwargs):
    #     self.user: User = kwargs.pop("user")
    #     super().__init__(*args, **kwargs)

    def render_answer(self, value, record: Question):
        correct_answers = record.correct_answers
        if len(correct_answers) == 0:
            return "ERROR - no correct answer specified!"
        correct_text = [a.text for a in correct_answers]
        return "\n".join(correct_text)

    def render_image(self, value, record: Question):
        return format_html(
            f"""<a href="" onclick="window.open('{record.image.url}','targetWindow', 'toolbar=no, location=no, status=no, menubar=no, scrollbars=yes, resizable=yes, width=800px, height=600px'); return false;">{value}</a>"""
        )

    def render_id(self, value, record: Question):
        if record.editable(user=self.request.user):
            return format_html(
                f'<a href="{reverse("mcq_bank:question_update", kwargs={"id": value})}">Edit question {value}</a>'
            )
        else:
            return format_html(
                f'<a href="{reverse("mcq_bank:question_detail", kwargs={"id": value})}">View question {value}</a>'
            )

    def render_answered(self, value, record: Question):
        return "Yes" if record.answered else "No"

    #
    # category_name = tables.Column(linkify=False, verbose_name="Category", orderable=False)
    # cat_qs_num = tables.Column(verbose_name="Nº questions total", empty_values=(), orderable=False)
    # attempted_num = tables.Column(verbose_name="Nº questions attempted", empty_values=(), orderable=False)
    # cat_average_score = tables.Column(verbose_name="Attempts correct avg (%)", empty_values=(), orderable=False)
    #
    # def render_attempted_num(self, value, record):
    #     return f"{value} ({record['attempted_percent'] or 0} %)"
    #
    # def render_cat_average_score(self, value, record):
    #     return f"{value or 0} %"


class QuestionListView(LoginRequiredMixin, ListView, tables.SingleTableMixin, FilterView):
    model = Question
    template_name = "mcq_bank/question_list.html"
    # form_class = QuestionCreateForm
    context_object_name = "question"
    lookup_field = "id"
    table_class = QuestionListTable

    def get_context_data(self, **kwargs):
        context = super(QuestionListView, self).get_context_data(**kwargs)
        all_questions = Question.objects.all()
        context["filter"] = QuestionListFilter(self.request.GET, queryset=all_questions)
        filtered_questions: QuerySet[Question] = context["filter"].qs
        answered_filter = self.parse_answered_filter(self.request.GET.get("answered"))
        annotated_questions = Question.question_list_for_user(user=self.request.user, questions=filtered_questions)
        if answered_filter is not None:
            annotated_questions = [q for q in annotated_questions if q.answered == answered_filter]

        context["question_list_table"] = QuestionListTable(annotated_questions, request=self.request)
        context["displayed_questions"] = annotated_questions
        context["quiz_create_form"] = QuizSessionCreateFromQuestionsForm(
            user=self.request.user, questions=annotated_questions
        )
        return context

    @staticmethod
    def parse_answered_filter(option: Optional[str]) -> Optional[bool]:
        mapping = {"-1": None, "1": True, "0": False, None: None, "": None}
        return mapping[option]
