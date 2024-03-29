from bootstrap_modal_forms.forms import BSModalModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Div, Field, Layout, Submit
from django import forms
from django.forms import Form
from django.forms.models import ModelForm, inlineformset_factory
from django.forms.widgets import CheckboxSelectMultiple, RadioSelect

from medusa_website.mcq_bank.models import Answer, Category, Question, QuizSession
from medusa_website.users.models import User
from medusa_website.utils.widgets import AuthorNameWidget, ImageDisplayWidget, RenderMarkdownWidget


class QuestionForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)

        choice_list = [x for x in question.get_answers_list()]
        self.fields["answers"] = forms.ChoiceField(choices=choice_list, widget=RadioSelect)

        self.helper = FormHelper()
        self.helper.form_id = "id-QuestionForm"
        # self.helper.form_class = "blueForms"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            # Div("categories", css_class="session-create-div"),
            # Div("max_num_questions", css_class="session-create-div"),
            # Div("include_answered", css_class="session-create-div"),
            Div("answers"),
            ButtonHolder(Submit("submit_answer", "Submit")),
        )


class QuestionDetailForm(ModelForm):
    class Meta:
        model = Question
        fields = [
            "author",
            "text",
            "category",
            "question_image",
            "answer_image",
            "explanation",
            "randomise_answer_order",
            "is_flagged",
            "is_reviewed",
            "flagged_by",
            "reviewed_by",
            "flagged_message",
        ]

    author = forms.CharField(label="Author", max_length=80, disabled=True, widget=AuthorNameWidget)
    explanation = forms.CharField(
        label="Explanation", max_length=500, disabled=True, widget=RenderMarkdownWidget(css_class="form-control")
    )

    question_image = forms.ImageField(label="Question Image", disabled=True, widget=ImageDisplayWidget)
    answer_image = forms.ImageField(label="Answer Image", disabled=True, widget=ImageDisplayWidget)


class QuestionUpdateForm(ModelForm):
    class Meta:
        model = Question
        fields = [
            "author",
            "text",
            "category",
            "question_image",
            "answer_image",
            "explanation",
            "randomise_answer_order",
            "is_flagged",
            "is_reviewed",
            "flagged_by",
            "reviewed_by",
            "flagged_message",
        ]

    # text = forms.CharField(widget=AdminPagedownWidget())
    # explanation = MartorFormField()
    # author = forms.CharField(label="Author", max_length=80, disabled=True, widget=AuthorNameWidget)

    def __init__(self, *args, **kwargs):
        if kwargs.get("id"):
            self.id = kwargs.pop("id")
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "id-question_update"

        for fieldname in ["is_flagged", "is_reviewed", "flagged_by", "reviewed_by", "flagged_message"]:
            self.fields[fieldname].help_text = None


class QuestionCreateForm(ModelForm):
    class Meta:
        model = Question
        fields = ["text", "category", "question_image", "answer_image", "explanation", "randomise_answer_order"]

    # explanation = forms.CharField(widget=AdminMartorWidget())

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


class AnswerInlineReadonlyForm(AnswerInlineForm):
    def __init__(self, *args, **kwargs):
        super(AnswerInlineReadonlyForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True


AnswerDetailFormSet = inlineformset_factory(
    Question, Answer, form=AnswerInlineReadonlyForm, extra=0, max_num=10, can_delete=False
)

AnswerCreateFormSet = inlineformset_factory(
    Question, Answer, form=AnswerInlineForm, extra=4, max_num=10, can_delete=False
)

AnswerUpdateFormSet = inlineformset_factory(
    Question, Answer, form=AnswerInlineForm, extra=0, max_num=10, can_delete=True
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


class QuizSessionCreateFromQuestionsForm(Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    questions = forms.ModelMultipleChoiceField(queryset=Question.objects.all())

    def __init__(self, user: User = None, questions=None, *args, **kwargs):

        super(QuizSessionCreateFromQuestionsForm, self).__init__(*args, **kwargs)
        if user:
            self.fields["user"].initial = user
        if questions:
            self.fields["questions"].initial = questions
        for field in self.fields.values():
            field.hidden = True

    def is_valid(self):
        return super(QuizSessionCreateFromQuestionsForm, self).is_valid()


class QuizSessionCreateForm(ModelForm):
    class Meta:
        model = QuizSession
        fields = []

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


class QuestionMarkFlaggedForm(ModelForm):
    class Meta:
        model = Question
        fields = ["id", "flagged_message"]

    def __init__(self, *args, **kwargs):
        super(QuestionMarkFlaggedForm, self).__init__(*args, **kwargs)

        self.fields["flagged_message"].help_text = None
