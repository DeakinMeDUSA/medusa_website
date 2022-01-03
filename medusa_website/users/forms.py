from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from cuser import forms as admin_forms
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import Form, ModelForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    error_message = admin_forms.UserCreationForm.error_messages.update(
        {"duplicate_email": _("This email has already been used.")}
    )

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

    def clean_email(self):
        email = self.cleaned_data["email"]

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email

        raise ValidationError(self.error_messages["duplicate_email"])


def validate_member_id(member_id):
    if not User.validate_member_id(member_id):
        raise ValidationError("Invalid member id. Should be the format of 20XX-XXXX-XX")


class MemberDetailForm(Form):
    class Meta:
        fields = ["member_id"]

    member_id = forms.CharField(label="Membership Number", max_length=12, validators=[validate_member_id])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_id = 'id-exampleForm'
        # self.helper.form_class = 'blueForms'
        self.helper.form_method = "post"
        # self.helper.form_action = 'submit_survey'
        self.helper.add_input(Submit("submit", "Submit"))
