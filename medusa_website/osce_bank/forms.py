from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field
from crispy_forms.layout import Layout, ButtonHolder, Submit
from django import forms
from django.forms import Form
from django.forms.models import ModelForm

from medusa_website.osce_bank.models import OSCEStation, Speciality, StationType, Level
from medusa_website.users.models import User
from medusa_website.utils.widgets import AuthorNameWidget, RenderMarkdownWidget, ImageDisplayWidget


class OSCEStationForm(forms.Form):
    def __init__(self, osce_station, *args, **kwargs):
        super(OSCEStationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = "id-OSCEStationForm"
        # self.helper.form_class = "blueForms"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            # Div("categories", css_class="session-create-div"),
            # Div("max_num_osce_stations", css_class="session-create-div"),
            # Div("include_answered", css_class="session-create-div"),
            ButtonHolder(Submit("submit_answer", "Submit")),
        )


class OSCEStationDetailForm(ModelForm):
    class Meta:
        model = OSCEStation
        fields = ["author", "title", "level", "types", "specialities", "stem", "patient_script", "marking_guide",
                  "supporting_notes", "stem_image", "marking_guide_image", "supporting_notes_image"]

    author = forms.CharField(label="Author", max_length=80, disabled=True, widget=AuthorNameWidget)
    stem = forms.CharField(
        label="Stem", disabled=True, widget=RenderMarkdownWidget(css_class="form-control")
    )
    patient_script = forms.CharField(
        label="Patient Script", disabled=True, widget=RenderMarkdownWidget(css_class="form-control")
    )
    marking_guide = forms.CharField(
        label="Marking Guide", disabled=True, widget=RenderMarkdownWidget(css_class="form-control")
    )
    supporting_notes = forms.CharField(
        label="Supporting Notes", disabled=True, widget=RenderMarkdownWidget(css_class="form-control")
    )
    specialities = forms.ModelMultipleChoiceField(
        queryset=Speciality.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        disabled=True)
    types = forms.ModelMultipleChoiceField(
        queryset=StationType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        disabled=True)

    stem_image = forms.ImageField(label="Stem Image", disabled=True, widget=ImageDisplayWidget)
    marking_guide_image = forms.ImageField(label="Marking Guide Image", disabled=True, widget=ImageDisplayWidget)
    supporting_notes_image = forms.ImageField(label="Supporting Notes Image", disabled=True, widget=ImageDisplayWidget)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True
            field.help_text = None
        self.helper = FormHelper()

class OSCEStationListForm(ModelForm):
    specialities = forms.ModelMultipleChoiceField(
        queryset=Speciality.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True)
    types = forms.ModelMultipleChoiceField(
        queryset=StationType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True)

    class Meta:
        model = OSCEStation
        fields = ["level", "types", "specialities", "is_flagged", "is_reviewed"]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper(self)
    #
    #     # self.helper.form_class = "blueForms"
    #     self.helper.form_tag = False
    #     self.helper.label_class = "font-weight-bold .text-warning"
    #
    #     for fieldname in ["stem", "patient_script", "marking_guide", "supporting_notes"]:
    #         self.fields[fieldname].help_text = None


class OSCEStationCreateUpdateForm(ModelForm):
    specialities = forms.ModelMultipleChoiceField(
        queryset=Speciality.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True)
    types = forms.ModelMultipleChoiceField(
        queryset=StationType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True)

    class Meta:
        model = OSCEStation
        fields = ["title", "level", "types", "specialities", "stem", "patient_script", "marking_guide",
                  "supporting_notes", "stem_image", "marking_guide_image", "supporting_notes_image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        # self.helper.form_class = "blueForms"
        self.helper.form_tag = False
        self.helper.label_class = "font-weight-bold .text-warning"

        for fieldname in ["stem", "patient_script", "marking_guide", "supporting_notes"]:
            self.fields[fieldname].help_text = None


class OSCESessionCreateFromOSCEStationsForm(Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    osce_stations = forms.ModelMultipleChoiceField(queryset=OSCEStation.objects.all())

    def __init__(self, user: User = None, osce_stations=None, *args, **kwargs):

        super(OSCESessionCreateFromOSCEStationsForm, self).__init__(*args, **kwargs)
        if user:
            self.fields["user"].initial = user
        if osce_stations:
            self.fields["osce_stations"].initial = osce_stations
        for field in self.fields.values():
            field.hidden = True

# class OSCESessionCreateForm(ModelForm):
#     class Meta:
#         model = OSCESession
#         fields = []
#
#     def __init__(self, *args, **kwargs):
#         # self.user = kwargs.pop("user")
#         self.helper = FormHelper()
#         self.helper.form_id = "id-exampleForm"
#         self.helper.form_class = "blueForms"
#         self.helper.form_method = "post"
#         self.helper.layout = Layout(
#             Div("categories", css_class="session-create-div"),
#             Div("max_num_stations", css_class="session-create-div"),
#             Div("include_completed", css_class="session-create-div"),
#             ButtonHolder(Submit("create_session", "Create OSCE Session")),
#         )
#         super(OSCESessionCreateForm, self).__init__(*args, **kwargs)
#
#     max_num_osce_stations = forms.ChoiceField(
#         label="Maximum number of stations",
#         choices=((5, "5"), (10, "10"), (20, "20")),
#         widget=forms.RadioSelect,
#         initial=5,
#         required=False,
#     )
#
#     # categories = forms.ModelMultipleChoiceField(
#     #     queryset=Category.objects.all(),
#     #     required=False,
#     #     label="Include osce_stations from categories",
#     #     widget=CheckboxSelectMultiple(attrs={"checked": ""}),  # All selected by default
#     # )
#
#     include_answered = forms.BooleanField(
#         label="Include already completed stations?",
#         required=False,
#         initial=False,
#     )
