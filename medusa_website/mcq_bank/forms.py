from bootstrap_modal_forms.forms import BSModalModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Div, Layout, Submit
from django import forms
from django.forms.models import ModelForm
from django.forms.widgets import CheckboxSelectMultiple, RadioSelect
from django.utils.safestring import mark_safe
from pagedown.widgets import AdminPagedownWidget

from medusa_website.mcq_bank.models import Category, Question, QuizSession
from medusa_website.users.models import User


class QuestionForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        choice_list = [x for x in question.get_answers_list()]
        self.fields["answers"] = forms.ChoiceField(choices=choice_list, widget=RadioSelect)


class AuthorNameWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        author = User.objects.get(id=value)
        return mark_safe(author.name) if value is not None else "-"


class QuestionDetailForm(ModelForm):
    class Meta:
        model = Question
        fields = ["author", "text", "category", "image", "explanation", "answer_order"]

    author = forms.CharField(label="Author", max_length=80, disabled=True, widget=AuthorNameWidget)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()


class QuestionUpdateForm(ModelForm):
    class Meta:
        model = Question
        fields = ["author", "text", "category", "image", "explanation", "answer_order"]

    text = forms.CharField(widget=AdminPagedownWidget())
    explanation = forms.CharField(widget=AdminPagedownWidget())

    def __init__(self, *args, **kwargs):
        self.editable: bool = kwargs.pop("editable")
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("update", "Update"))
        if self.editable is False:
            self.author = forms.CharField(label="Author", max_length=80, disabled=True, widget=AuthorNameWidget)


class QuestionCreateForm(forms.Form):
    class Meta:
        model = Question
        fields = ["text", "category", "image", "explanation", "answer_order"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Submit"))


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
