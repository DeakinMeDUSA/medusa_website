from colorfield.fields import ColorField
from django.db import models
from tinymce import models as tinymce_models

from medusa_website.users.models import User


class SubCommittee(models.Model):
    title = models.CharField(max_length=128, unique=True)
    org_chart_fill_color = ColorField(default="#000000", help_text="Should be a CSS compatible hex colour")
    explanation_text = tinymce_models.HTMLField(default="")

    def __repr__(self):
        return f"<{self.__class__.__name__}> - {self.title}"

    def __str__(self):
        return self.__repr__()


class CommitteeRole(models.Model):
    position = models.CharField(max_length=128, help_text="Name of the position", unique=True)
    email = models.EmailField(help_text="Must not be the personal email of the position holder")
    sub_committee = models.ForeignKey(
        to=SubCommittee,
        on_delete=models.CASCADE,
        related_name="members",
        help_text="Subcommittee the position belongs to",
    )

    def __repr__(self):
        return f"<{self.__class__.__name__} - {self.position} - {self.email}>"

    def __str__(self):
        return self.__repr__()


class CommitteeRoleRecord(models.Model):
    """
    Represents a year of holding a position on the committee for a particular year.
    """

    role = models.ForeignKey(CommitteeRole, on_delete=models.PROTECT, related_name="history")
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="committee_member_records")
    year = models.IntegerField(help_text="Year that the user held this position in the committee")

    class Meta:
        unique_together = ["role", "user", "year"]

    def __repr__(self):
        return f"<{self.__class__.__name__} - {self.role.position} - {self.user} - {self.year}>"

    def __str__(self):
        return self.__repr__()
