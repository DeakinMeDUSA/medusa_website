from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from nameparser import HumanName

from medusa_website.users.validators import CustomEmailValidator


class AccountAdapter(DefaultAccountAdapter):
    custom_email_validators = CustomEmailValidator

    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def clean_email(self, email):
        """
        Validates an email value. You can hook into this if you want to
        (dynamically) restrict what email addresses can be chosen.
        """
        email = email.lower()
        try:
            for validator in self.custom_email_validators:
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

        user: User = super(AccountAdapter, self).save_user(request, user, form, commit=False)

        # Try to get first and last name's from MemberRecords
        try:
            member_record = MemberRecord.objects.get(email=user.email)
            member_name = HumanName(member_record.name)
            member_name.capitalize(force=True)
            user.name = member_name
        except MemberRecord.DoesNotExist:
            pass

        user_part, domain_part = user.email.rsplit("@", 1)
        if domain_part == "medusa.org.au":
            user.is_medusa = True

        if commit:
            user.save()
        return user


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
