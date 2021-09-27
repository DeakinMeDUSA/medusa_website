from typing import Optional

import markdown
from django.db import models
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.safestring import mark_safe
from martor.models import MartorField
from memoize import memoize

from medusa_website.users.models import User


class Level(models.Model):
    class Meta:
        ordering = ('level',)

    level = models.CharField(help_text="The year level appropriate for the OSCE station", max_length=128, unique=True)

    def __str__(self):
        return self.level


class StationType(models.Model):
    class Meta:
        ordering = ('station_type',)

    station_type = models.CharField(help_text="The type of OSCE station, e.g. Examination", max_length=128, unique=True)

    def __str__(self):
        return self.station_type


class Speciality(models.Model):
    class Meta:
        verbose_name = "Speciality"
        verbose_name_plural = "Specialities"
        ordering = ('speciality',)

    speciality = models.CharField(help_text="A speciality for the Station/MCQ OSCEStation e.g. Cardiology",
                                  max_length=128,
                                  unique=True)

    def __str__(self):
        return self.speciality


class OSCEStation(models.Model):
    class Meta:
        verbose_name = "OSCE Station"
        verbose_name_plural = "OSCE Stations"

    title = models.CharField(max_length=128, unique=True, help_text="The title of the OSCE station")
    level = models.ForeignKey(Level, on_delete=models.PROTECT, related_name="stations")
    types = models.ManyToManyField(StationType)
    specialities = models.ManyToManyField(Speciality)
    author = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)

    stem = MartorField(
        help_text="OSCE Stem to be shown to the candidate completing the station",
    )
    patient_script = MartorField(
        help_text="Patient script for the person acting as patient",
    )
    marking_guide = MartorField(
        help_text="Marking guide for the station", blank=True, null=True,
    )
    supporting_notes = MartorField(
        help_text="Supporting notes for the station", blank=True, null=True,
    )

    is_flagged = models.BooleanField(default=False,
                                     help_text="If True, has been flagged by a user and is awaiting review")
    flagged_by = models.ForeignKey(
        User, related_name="flagged_osce_stations", on_delete=models.PROTECT, blank=True, null=True
    )
    flagged_message = models.TextField(null=True, blank=True, help_text="Explanation for why the station was flagged.")

    is_reviewed = models.BooleanField(default=False, help_text="If True, has been reviewed by a staff or admin")
    reviewed_by = models.ForeignKey(
        User, related_name="reviewed_osce_stations", on_delete=models.PROTECT, blank=True, null=True
    )

    stem_image = models.ImageField(
        null=True, blank=True, verbose_name="Stem image",
        help_text="Upload an image to be shown in the OSCE station stem"
    )
    marking_guide_image = models.ImageField(
        null=True, blank=True, verbose_name="Marking Guide image",
        help_text="Upload an image to be shown with the marking guide"
    )
    supporting_notes_image = models.ImageField(
        null=True, blank=True, verbose_name="Further Notes image",
        help_text="Upload an image to be shown alongside the supporting notes"
    )

    def __str__(self):
        return self.title

    @property
    def stem_image_url(self) -> Optional[str]:
        return self.stem_image.url if self.stem_image else None

    @property
    def marking_guide_image_url(self) -> Optional[str]:
        return self.marking_guide_image.url if self.marking_guide_image else None

    @property
    def supporting_notes_image_url(self) -> Optional[str]:
        return self.supporting_notes_image.url if self.supporting_notes_image else None

    def is_completed(self, user: User) -> bool:
        return self in user.osce_history.completed_stations.all()

    @classmethod
    @memoize(timeout=60)  # cache result for 60 seconds
    def station_list_for_user(cls, user=User, stations: Optional[QuerySet] = None):
        """For use in the station_list view"""
        from medusa_website.osce_bank.models.history import OSCEHistory

        history, created = OSCEHistory.objects.get_or_create(user=user)  # force init of history
        completed_stations = history.completed_stations.all()
        all_stations = stations if stations is not None else cls.objects.all()
        for s in all_stations:
            s.completed = True if s in completed_stations else False
        return all_stations

    @property
    def stem_as_html(self):
        if self.stem:
            html = markdown.markdown(self.stem)
            return mark_safe(html)
        else:
            return mark_safe("<i>No stem provided</i>")

    @property
    def patient_script_as_html(self):
        if self.patient_script:
            html = markdown.markdown(self.patient_script)
            return mark_safe(html)
        else:
            return mark_safe("<i>No patient script provided</i>")

    @property
    def marking_guide_as_html(self):
        if self.marking_guide:
            html = markdown.markdown(self.marking_guide)
            return mark_safe(html)
        else:
            return mark_safe("<i>No marking guide provided</i>")

    @property
    def supporting_notes_as_html(self):
        if self.supporting_notes:
            html = markdown.markdown(self.supporting_notes)
            return mark_safe(html)
        else:
            return mark_safe("<i>No supporting notes provided</i>")

    def editable(self, user: User):
        # return user.is_staff or user.is_superuser or (user == self.author)
        return True

    def get_absolute_url(self):
        return reverse("osce_bank:osce_station_detail", kwargs={"id": self.id})
