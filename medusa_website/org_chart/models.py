from colorfield.fields import ColorField
from django.db import models
from tinymce import models as tinymce_models


class SubCommittee(models.Model):
    title = models.CharField(max_length=128, unique=True)
    org_chart_fill_color = ColorField(default="#000000", help_text="Should be a CSS compatible hex colour")
    explanation_text = tinymce_models.HTMLField(default="")

    def __repr__(self):
        return f"<{self.__class__.__name__}> - {self.title}"

    def __str__(self):
        return self.__repr__()


class CommitteeMember(models.Model):
    name = models.CharField(max_length=128, help_text="Name of the current holder of the position")
    position = models.CharField(max_length=128, help_text="Name of the position", unique=True)
    email = models.EmailField(help_text="Must be a medusa.org.au email, not the personal email of the position holder")
    sub_committee = models.ForeignKey(
        to=SubCommittee,
        on_delete=models.CASCADE,
        related_name="members",
        help_text="Subcommittee the position belongs to",
    )
    profile_pic = models.ImageField(
        upload_to="org_chart/images", null=True, blank=True, help_text="Profile pic of the current committee member"
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}> - {self.position} - {self.name}"

    def __str__(self):
        return self.__repr__()
