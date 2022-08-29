from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.http import HttpRequest
from django.utils.safestring import mark_safe
from nameparser import HumanName

from medusa_website.users.validators import MedusaMemberValidator
from medusa_website.utils.general import get_pretty_logger

logger = get_pretty_logger(__name__)


class AccountAdapter(DefaultAccountAdapter):
    email_validators = [
        EmailValidator(),
        MedusaMemberValidator(),
    ]
    error_messages = DefaultAccountAdapter.error_messages
    error_messages["email_taken"] = mark_safe(
        "The supplied email was found to match an existing user. <br>"
        "This user may have been generated automatically without a password, please visit "
        '<a href="https://www.medusa.org.au/accounts/password/reset/">the password reset page</a> to set a new one.'
    )

    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def clean_email(self, email):
        """
        Validates an email value. You can hook into this if you want to
        (dynamically) restrict what email addresses can be chosen.
        """
        email = email.lower()
        try:
            for validator in self.email_validators:
                validator(email)
        except ValidationError as errmsg:
            raise forms.ValidationError(errmsg)
        return email

    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        from medusa_website.users.models import MemberRecord, User

        # Uses medusa_website.users.validators.CustomSignupEmailValidator
        user: User = super().save_user(request, user, form, commit=True)

        # Try to get first and last name's from MemberRecords
        # A member record should already have been verified to exist using the custom_email_validators
        try:
            member_record = MemberRecord.objects.get(email=user.email)
            user.is_member = True
            user.create_member_id()
            user.membership_expiry = member_record.end_date
            member_name = HumanName(member_record.name)
            member_name.capitalize(force=True)
            user.name = member_name
        except MemberRecord.DoesNotExist:
            logger.warning(f"Member Record for {user.email} does not exist")

        user_part, domain_part = user.email.rsplit("@", 1)
        if domain_part == "medusa.org.au":
            user.is_medusa = True
            user.is_member = False
            user.is_staff = True

        if commit:
            user.save()
        return user


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
