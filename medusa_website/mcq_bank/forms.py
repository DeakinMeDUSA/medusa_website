import markdown
from bootstrap_modal_forms.forms import BSModalModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field
from crispy_forms.layout import Layout, ButtonHolder, Submit
from django import forms
from django.forms.models import ModelForm, inlineformset_factory
from django.forms.widgets import CheckboxSelectMultiple, RadioSelect
from django.utils.safestring import mark_safe
from martor.widgets import AdminMartorWidget

from medusa_website.mcq_bank.models import Category, Question, QuizSession, Answer
from medusa_website.users.models import User


class QuestionForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        choice_list = [x for x in question.get_answers_list()]
        self.fields["answers"] = forms.ChoiceField(choices=choice_list, widget=RadioSelect)


class AuthorNameWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        if value:
            author = User.objects.get(id=value)
            return mark_safe(f"<b>{author.name}</b>") if value is not None else "-"
        else:
            return mark_safe("-")


class RenderMarkdownWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        if value:
            html = markdown.markdown(value)
            return mark_safe(html)
        else:
            return mark_safe("None")


class QuestionDetailForm(ModelForm):
    class Meta:
        model = Question
        fields = ["author", "text", "category", "image", "explanation", "randomise_answer_order"]

    author = forms.CharField(label="Author", max_length=80, disabled=True, widget=AuthorNameWidget)
    explanation = forms.CharField(label="Explanation", max_length=500, disabled=True, widget=RenderMarkdownWidget)
    image = forms.ImageField(label="image", disabled=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('author', readonly=True),
            Field("text", readonly=True),
            Field("category", readonly=True),
            Field("image", readonly=True),
            Field("explanation", readonly=True),
            Field("randomise_answer_order", readonly=True)
        )


class QuestionUpdateForm(ModelForm):
    class Meta:
        model = Question
        fields = ["author", "text", "category", "image", "explanation", "randomise_answer_order"]

    # text = forms.CharField(widget=AdminPagedownWidget())
    # explanation = forms.CharField(widget=AdminPagedownWidget())
    # author = forms.CharField(label="Author", max_length=80, disabled=True, widget=AuthorNameWidget)

    def __init__(self, *args, **kwargs):
        if kwargs.get("id"):
            self.id = kwargs.pop("id")
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "id-question_update"


class QuestionCreateForm(ModelForm):
    class Meta:
        model = Question
        fields = ["text", "category", "image", "explanation", "randomise_answer_order"]

    explanation = forms.CharField(widget=AdminMartorWidget())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        # self.helper.form_class = "blueForms"
        self.helper.form_tag = False
        self.helper.label_class = "font-weight-bold .text-warning"


class AnswerInlineForm(ModelForm):
    class Meta:
        model = Answer
        fields = ["text", "correct", "explanation"]
        help_texts = {"text": None, "correct": None, "explanation": None}


AnswerCreateFormSet = inlineformset_factory(
    Question, Answer, fields=["text", "correct", "explanation"], extra=4, max_num=10,
    can_delete=False
)

AnswerUpdateFormSet = inlineformset_factory(
    Question, Answer, fields=["text", "correct", "explanation"], extra=0, max_num=10,
    can_delete=True
)


class AnswerFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template = "mcq_bank/table_inline_formset.html"
        self.form_tag = False
        self.form_group_wrapper_class = "answer-table"


class QuizSessionContinueOrStopForm(BSModalModelForm):
    class Meta:
        model = QuizSession
        fields = ["user", "complete"]


class QuizSessionCreateForm(ModelForm):
    class Meta:
        model = QuizSession
        fields = []

    def __init__(self, *args, **kwargs):
        # self.user = kwargs.pop("user")
        self.helper = FormHelper()
        self.helper.form_id = "id-exampleForm"
        self.helper.form_class = "blueForms"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Div("categories", css_class="session-create-div"),
            Div("max_num_questions", css_class="session-create-div"),
            Div("include_answered", css_class="session-create-div"),
            Div("randomise_order", css_class="session-create-div"),
            ButtonHolder(Submit("create_session", "Create Quiz Session")),
        )
        super(QuizSessionCreateForm, self).__init__(*args, **kwargs)

    max_num_questions = forms.ChoiceField(
        label="Maximum number of questions",
        choices=((10, "10"), (50, "50"), (100, "100")),
        widget=forms.RadioSelect,
        initial=10,
        required=False,
    )

    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label="Include questions from categories",
        widget=CheckboxSelectMultiple(attrs={"checked": ""}),  # All selected by default
    )

    include_answered = forms.BooleanField(
        label="Include already answered questions?",
        required=False,
        initial=False,
    )
    randomise_order = forms.BooleanField(
        label="Randomise the order of the questions?",
        required=False,
        initial=True,
    )
