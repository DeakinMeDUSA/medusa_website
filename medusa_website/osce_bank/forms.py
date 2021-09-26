from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit
from django import forms
from django.forms import Form
from django.forms.models import ModelForm

from medusa_website.osce_bank.models import OSCEStation, Speciality, StationType
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
                  "supporting_notes", "stem_image", "marking_guide_image", "supporting_notes_image",
                  "is_flagged", "is_reviewed", "flagged_by", "reviewed_by", "flagged_message"]

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


class OSCEStationCreateForm(ModelForm):
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


class OSCEStationUpdateForm(OSCEStationCreateForm):
    class Meta:
        model = OSCEStation
        fields = ["title", "level", "types", "specialities", "stem", "patient_script", "marking_guide",
                  "supporting_notes", "stem_image", "marking_guide_image", "supporting_notes_image",
                  "is_flagged", "is_reviewed", "flagged_by", "reviewed_by", "flagged_message"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        # self.helper.form_class = "blueForms"
        self.helper.form_tag = False
        self.helper.label_class = "font-weight-bold .text-warning"

        for fieldname in ["stem", "patient_script", "marking_guide", "supporting_notes",
                          "is_flagged", "is_reviewed", "flagged_by", "reviewed_by", "flagged_message"]:
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


class OSCEStationCompleteForm(ModelForm):
    class Meta:
        model = OSCEStation
        fields = ["id"]

    # osce_station = forms.ModelChoiceField(queryset=OSCEStation.objects.all())

    def __init__(self, *args, **kwargs):
        super(OSCEStationCompleteForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.hidden = True


class OSCEStationMarkFlaggedForm(ModelForm):
    class Meta:
        model = OSCEStation
        fields = ["id", "flagged_message"]

    # osce_station = forms.ModelChoiceField(queryset=OSCEStation.objects.all())

    def __init__(self, *args, **kwargs):
        super(OSCEStationMarkFlaggedForm, self).__init__(*args, **kwargs)

        self.fields["flagged_message"].help_text = None
