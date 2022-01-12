from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils.safestring import mark_safe

from medusa_website.users.models import MemberRecord


class ExistingUserValidator:
    message = mark_safe(
        "The supplied email was found to match an existing user. <br>"
        "This user may have been generated automatically without a password, please visit "
        '<a href="https://www.medusa.org.au/accounts/password/reset/">the password reset page</a> to set a new one.'
    )

    code = "invalid"

    def __init__(self, message=None, code=None, whitelist=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        if whitelist is not None:
            self.domain_whitelist = whitelist

    def __call__(self, value):
        if self.validate_existing_user_status(value) is False:
            raise ValidationError(self.message, code=self.code)

    def validate_existing_user_status(self, email: str):
        try:
            from medusa_website.users.models import User

            User.objects.get(email=email.lower())
            return False
        except User.DoesNotExist:
            return True

    def __eq__(self, other):
        return (
            isinstance(other, MedusaMemberValidator) and (self.message == other.message) and (self.code == other.code)
        )


class MedusaMemberValidator:
    message = mark_safe(
        "The supplied email was not found on member list supplied by DUSA, which is updated weekly. <br>"
        'If you believe this to be an error, please contact <a href="mailto:it@medusa.org.au">it@medusa.org.au</a>'
    )

    code = "invalid"
    domain_whitelist = ["medusa.org.au", "dusa.org.au"]

    def __init__(self, message=None, code=None, whitelist=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        if whitelist is not None:
            self.domain_whitelist = whitelist

    def __call__(self, value):
        try:
            user_part, domain_part = value.rsplit("@", 1)
        except ValueError:
            raise ValidationError(self.message, code=self.code)

        if self.validate_domain_part(domain_part) is False and self.validate_member_status(value) is False:
            raise ValidationError(self.message, code=self.code)

    def validate_member_status(self, email: str):
        try:
            MemberRecord.objects.get(email=email.lower())
            return True
        except MemberRecord.DoesNotExist:
            return False

    def validate_domain_part(self, domain_part):
        return domain_part in self.domain_whitelist

    def __eq__(self, other):
        return (
            isinstance(other, MedusaMemberValidator)
            and (self.domain_whitelist == other.domain_whitelist)
            and (self.message == other.message)
            and (self.code == other.code)
        )


CustomEmailValidator = [EmailValidator(), MedusaMemberValidator(), ExistingUserValidator()]
