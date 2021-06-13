from itertools import islice

import openpyxl
import pandas as pd
from allauth.account.models import EmailAddress
from cuser.models import AbstractCUser, CUser
from django.conf import settings
from django.db import models
from django.db.models import CharField, EmailField, IntegerField, ManyToManyField
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(AbstractCUser):
    """Default user for MeDUSA Website."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    graduation_year = IntegerField(
        verbose_name="Year of Graduation", null=True, blank=True
    )

    REQUIRED_FIELDS = ["name", "graduation_year"]

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"email": self.email})

    @property
    def answered_questions(self):
        from medusa_website.mcq_bank.models import Record

        return Record.objects.filter(user=self)

    @property
    def correct_questions(self):
        return self.answered_questions.filter(answer__is_correct=True)

    @property
    def incorrect_questions(self):
        return self.answered_questions.filter(answer__is_correct=False)

    @property
    def all_emails(self):
        return EmailAddress.objects.filter(user=self).all()


class MemberRecord(models.Model):
    email = EmailField(primary_key=True, unique=True)
    name = CharField(blank=True, null=True, max_length=256)
    end_date = models.DateField(_("end date"))
    import_records = ManyToManyField("MemberRecordsImport")


class MemberRecordsImport(models.Model):
    """ Represents a membership record from the DUSA exports"""

    members = ManyToManyField(MemberRecord)
    import_dt = models.DateTimeField(_("import time"), default=timezone.now)

    @staticmethod
    def create_from_export():
        print(f"Starting import of memberlist...")
        memberlist_excel = openpyxl.load_workbook(settings.MEMBERLIST_XLSX)
        memberlist_sheet = memberlist_excel["Report"]
        new_import = MemberRecordsImport()
        new_import.save()
        data = memberlist_sheet.values
        cols = next(data)[0:]
        data = list(data)
        data = (islice(r, 0, None) for r in data)
        df = pd.DataFrame(data, index=None, columns=cols)
        print(f"df = {df.head()}")
        for idx, row in df.iterrows():
            member, created = MemberRecord.objects.update_or_create(
                email=row["Email"], name=row["Full Name"], end_date=row["End Date"]
            )
            member.import_records.add(new_import)

        print(f"Finished import of memberlist!")
