from django.db import models

from medusa_website.utils.general import get_pretty_logger

logger = get_pretty_logger(__name__)


class ContributionType(models.Model):
    """
    A type of contribution, e.g MCQ Night
    """

    machine_name = models.CharField(
        max_length=64,
        help_text="Machine readable type of contribution, e.g. MCQ_NIGHT_ORGANISE. Must be unique",
        unique=True,
    )
    name = models.CharField(
        max_length=128,
        help_text="Human readable type of contribution, e.g. 'Organised MCQ Night'. Must be unique.",
        unique=True,
    )
    template = models.CharField(
        max_length=128,
        help_text="Template for certificate, use $COUNT to replace with count of that "
        "contribution. E.g 'Creating $COUNT MCQ Bank Questions'",
        null=True,
        blank=True,
    )
    subtype = models.CharField(
        max_length=128, choices=[("WEBSITE", "WEBSITE"), ("EVENTS", "EVENTS"), ("OTHER", "OTHER")], default="OTHER"
    )
    requires_signoff = models.BooleanField(
        default=True, help_text="True if this contribution requires signoff by a executive member"
    )
    signoff_requirements = models.TextField(
        help_text="Any sign off requirements for the contribution, e.g. uploading MCQ slides to MeDUSA drive",
        null=True,
        blank=True,
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.machine_name}>"

    def __str__(self):
        return self.__repr__()
