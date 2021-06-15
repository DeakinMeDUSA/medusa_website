import django_tables2 as tables
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.html import format_html
from vanilla import CreateView, DetailView, ListView, UpdateView

from medusa_website.mcq_bank.forms import (
    QuestionCreateForm,
    QuestionDetailForm,
    QuestionUpdateForm,
)
from medusa_website.mcq_bank.models import Question
from medusa_website.users.models import User


class QuestionUpdateView(DetailView, UpdateView, LoginRequiredMixin):
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
        return context

    def form_valid(self, form):
        if isinstance(form.cleaned_data["author"], User) is False:
            print(f"Author came in as {form.cleaned_data['author']}, resetting to prior value: {form.instance.user}")
            form.cleaned_data["author"] = form.instance.author
        return super(QuestionUpdateView, self).form_valid(form)

    @staticmethod
    def editable(user, question):
        return user.is_staff or question.author == user


class QuestionCreateView(CreateView, LoginRequiredMixin):
    model = Question
    template_name = "mcq_bank/question_create.html"
    form_class = QuestionCreateForm
    context_object_name = "question"
    lookup_field = "id"
    success_url = reverse_lazy("mcq_bank:question_list")

    def form_valid(self, form):
        print(form)
        return super(QuestionCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        user = request.user

        return super(QuestionCreateView, self).post(request, *args, **kwargs)


class QuestionListTable(tables.Table):
    class Meta:
        attrs = {
            "class": "table tablesorter-metro-dark",  # Sorting is handled by js to avoid refresh
            "id": "question-list-table",
        }
        model = Question
        exclude = ("answer_order",)
        sequence = ("id", "author", "category", "text", "answer", "explanation", "image")

    id = tables.Column(linkify=True, accessor="id", orderable=False)
    author = tables.Column(linkify=True, orderable=False)
    category = tables.Column(linkify=True, orderable=False)
    text = tables.Column(linkify=False, orderable=False)
    answer = tables.Column(linkify=False, orderable=False, empty_values=(), verbose_name="Answer")
    explanation = tables.Column(linkify=False, orderable=False)
    image = tables.Column(linkify=False, orderable=False)

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


class QuestionListView(ListView, LoginRequiredMixin, tables.SingleTableMixin):
    model = Question
    template_name = "mcq_bank/question_list.html"
    # form_class = QuestionCreateForm
    context_object_name = "question"
    lookup_field = "id"
    table_class = QuestionListTable

    def get_context_data(self, **kwargs):
        context = super(QuestionListView, self).get_context_data(**kwargs)
        questions = Question.objects.all()
        context["question_list_table"] = QuestionListTable(questions)
        return context
