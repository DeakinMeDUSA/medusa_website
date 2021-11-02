from django.db import models

from medusa_website.users.models import User


class ContributionType(models.TextChoices):
    MCQ_NIGHT = ('MCQ', "MCQ Night")


class Contribution(models.Model):
    """
    Represents a Student's contribution to MeDUSA that isn't covered by one of the existing models
    """
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="contribution")
    contrib_type = models.CharField(verbose_name="Contribution type", max_length=128, choices=ContributionType.choices)
    title = models.CharField(max_length=192, help_text="Title / name of the contribution")
    completed_date = models.DateField(
        help_text="Date the contribution was completed. If it was over multiple date, give the last date")
    submitted_date = models.DateField(auto_now_add=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="reviewed_contributions", null=True,
                                    blank=True)
    is_reviewed = models.BooleanField(default=False)
