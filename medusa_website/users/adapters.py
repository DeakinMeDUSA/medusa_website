from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import HttpRequest

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
        try:
            for validator in self.custom_email_validators:
                validator(email)
        except ValidationError as errmsg:
            raise forms.ValidationError(errmsg)
        return email


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
