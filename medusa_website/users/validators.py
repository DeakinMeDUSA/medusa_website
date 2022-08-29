import datetime

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils.safestring import mark_safe

from medusa_website.users.models import MemberRecord, MemberRecordsImport


class MedusaMemberValidator:
    code = "invalid"
    domain_whitelist = ["medusa.org.au", "dusa.org.au"]

    def __init__(self):
        pass

    @property
    def message(self) -> str:
        most_recent_import = MemberRecordsImport.objects.last().import_dt.date()
        return mark_safe(
            f"The supplied email was not found on member list supplied by DUSA. <br>"
            f"This list is updated weekly, and was last updated {most_recent_import}.<br>"
            'If you believe this to be an error, please contact <a href="mailto:it@medusa.org.au">it@medusa.org.au</a>'
        )

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


CustomSignupEmailValidator = [EmailValidator(), MedusaMemberValidator()]
