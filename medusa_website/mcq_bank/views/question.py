from pprint import pprint
from typing import Optional

import django_tables2 as tables
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.html import format_html
from django_filters import FilterSet
from django_filters.views import FilterView
from extra_views import InlineFormSetFactory, CreateWithInlinesView, NamedFormsetsMixin, SuccessMessageMixin
from vanilla import ListView, UpdateView

from medusa_website.mcq_bank.forms import (
    QuestionCreateForm,
    QuestionDetailForm,
    QuestionUpdateForm,
    AnswerCreateFormSetHelper,
    AnswerCreateForm,
)
from medusa_website.mcq_bank.models import Question, Answer
from medusa_website.users.models import User


class QuestionUpdateView(UpdateView, LoginRequiredMixin):
    model = Question
    template_name = "mcq_bank/question_update.html"
    form_class = QuestionDetailForm
    context_object_name = "question"
    lookup_field = "id"
    success_url = reverse_lazy("mcq_bank:question_list")

    def get_template_names(self):
        editable = self.editable(self.request.user, self.get_object())
        if editable:
            self.template_name = "mcq_bank/question_update.html"
        else:
            self.template_name = "mcq_bank/question_view.html"
        return super(QuestionUpdateView, self).get_template_names()

    def get_form(self, data=None, files=None, **kwargs):
        editable = self.editable(self.request.user, self.get_object())
        if self.request.method == "GET" and editable is False:
            return QuestionDetailForm(data, files, **kwargs)  # Just view the question
        else:
            return QuestionUpdateForm(data, files, editable=editable, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(QuestionUpdateView, self).get_context_data(**kwargs)
        context["editable"] = self.editable(self.request.user, question=self.get_object())
        context["question_update_form"] = self.get_form(**kwargs)
        return context

    def form_valid(self, form):
        if isinstance(form.cleaned_data["author"], User) is False:
            print(f"Author came in as {form.cleaned_data['author']}, resetting to prior value: {form.instance.user}")
            form.cleaned_data["author"] = form.instance.author
        return super(QuestionUpdateView, self).form_valid(form)

    @staticmethod
    def editable(user, question):
        return user.is_staff or question.author == user


class AnswerInline(InlineFormSetFactory):
    model = Answer
    form_class = AnswerCreateForm
    # fields = ["question", "text", "correct", "explanation"]
    factory_kwargs = {"extra": 4, "max_num": 10, "can_order": False, "can_delete": False}

    # TODO fix Question_create javascript to add answers again


#     template_name = "mcq_bank/question_create.html"
class QuestionCreateView(CreateWithInlinesView, LoginRequiredMixin, NamedFormsetsMixin, SuccessMessageMixin):
    model = Question
    inlines = [
        AnswerInline,
    ]
    inlines_names = [
        "answer_formset",
    ]

    # fields = ["text", "category", "image", "explanation", "randomise_answer_order"]
    template_name = "mcq_bank/question_create.html"
    form_class = QuestionCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # formset = modelformset_factory(Answer, form=AnswerCreateForm, extra=2)
        context["answer_formset_helper"] = AnswerCreateFormSetHelper()
        # context["formset"] = formset
        pprint(context)

        return context

    def forms_valid(self, form: QuestionCreateForm, inlines):
        answer_formset = inlines[0]
        # Check at least two answers provided
        complete_answers = []
        complete_answer_forms = []
        incomplete_answer_forms = []
        answer_form: AnswerCreateForm
        for answer_form in answer_formset.forms:
            temp_a: Answer = answer_form.save(commit=False)
            if temp_a.text and len(temp_a.text) > 0:
                complete_answers.append(temp_a)
                complete_answer_forms.append(answer_form)
            else:
                incomplete_answer_forms.append(answer_form)
        answer_texts = set([ans.text for ans in complete_answers])

        if len(complete_answers) < 2:
            for answer_form in incomplete_answer_forms:
                answer_form.add_error(field="text", error="Two or more answers must be specified")
            return self.render_to_response(self.get_context_data(form=form, inlines=inlines))
        elif len(complete_answers) > 10:
            for answer_form in complete_answer_forms[9:]:
                answer_form.add_error(field="text", error="A maximum of 10 answers can be specified")
            return self.render_to_response(self.get_context_data(form=form, inlines=inlines))
        elif len([ans for ans in complete_answers if ans.correct]) != 1:
            for answer_form in complete_answer_forms:
                answer_form.add_error(field="text", error="There must be exactly one correct answer specified")
            return self.render_to_response(self.get_context_data(form=form, inlines=inlines))
        elif len(answer_texts) != len(complete_answers):
            for answer_form in complete_answer_forms:
                answer_form.add_error(field="text", error="All answers must be unique for a particular question!")
            return self.render_to_response(self.get_context_data(form=form, inlines=inlines))

        else:
            question = form.save(commit=False)
            question.author = self.request.user
            question.save()
            for ans in complete_answers:
                ans.save()
            question.answers.set(complete_answers)
            question.save()
            self.object = question
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_success_message(self, cleaned_data, inlines):
        return f"Question with id {self.object.pk} successfully created"


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
        exclude = ("randomise_answer_order",)
        sequence = ("id", "author", "category", "answered", "text", "answer", "explanation", "image")

    id = tables.Column(linkify=True, accessor="id", orderable=False)
    author = tables.Column(linkify=True, orderable=False)
    category = tables.Column(linkify=True, orderable=False)
    answered = tables.Column(linkify=False, orderable=False, empty_values=())
    text = tables.Column(linkify=False, orderable=False)
    answer = tables.Column(linkify=False, orderable=False, empty_values=(), verbose_name="Answer")
    explanation = tables.Column(linkify=False, orderable=False)
    image = tables.Column(linkify=False, orderable=False)
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
        return f"View/edit question {value}"

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


class QuestionListView(ListView, LoginRequiredMixin, tables.SingleTableMixin, FilterView):
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
        print(f"answered_filter = {answered_filter} | request.GET.answered = {self.request.GET.get('answered')}")
        print(f"request.GET = {self.request.GET}")
        annotated_questions = Question.question_list_for_user(user=self.request.user, questions=filtered_questions)
        if answered_filter is not None:
            annotated_questions = [q for q in annotated_questions if q.answered == answered_filter]

        context["question_list_table"] = QuestionListTable(annotated_questions)
        return context

    @staticmethod
    def parse_answered_filter(option: Optional[str]) -> Optional[bool]:
        mapping = {"-1": None, "1": True, "0": False, None: None, "": None}
        return mapping[option]
