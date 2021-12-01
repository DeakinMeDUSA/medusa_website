from itertools import islice

import openpyxl
import pandas as pd
from django.db import models
from django.db.models import CharField, EmailField, ManyToManyField


class MemberRecord(models.Model):
    email = EmailField(primary_key=True, unique=True)
    name = CharField(blank=True, null=True, max_length=256)
    end_date = models.DateField("End date")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.email = self.email.lower()
        super(MemberRecord, self).save()


class MemberRecordsImport(models.Model):
    """Represents a membership record from the DUSA exports"""

    members = ManyToManyField(MemberRecord, blank=True, related_name="member_record_imports")
    import_dt = models.DateTimeField("Import time", auto_now_add=True)
    report_date = models.DateField(help_text="Date the report was generated", unique=True)
    file = models.FileField(upload_to="dusa_reports/%Y", null=True, blank=True)

    def import_memberlist(self) -> pd.DataFrame:
        print(f"Starting import of memberlist...")
        memberlist_excel = openpyxl.load_workbook(self.file.path)
        memberlist_sheet = memberlist_excel["Report"]
        data = memberlist_sheet.values
        cols = next(data)[0:]
        data = list(data)
        data = (islice(r, 0, None) for r in data)
        df = pd.DataFrame(data, index=None, columns=cols)
        print(f"df = {df}")
        for idx, row in df.iterrows():
            member, created = MemberRecord.objects.update_or_create(
                email=row["Email"],
                defaults={
                    "email": row["Email"],
                    "name": row["Full Name"],
                    "end_date": row["End Date"]}
            )
            member.member_record_imports.add(self)
            member.save()

        print(f"Finished import of member list!")
        return df

    #
    # def export_csv(self, pth: Path = None) -> pd.DataFrame:
    #     google_export = pd.DataFrame(columns=["Member Email", "Member Type", "Member Role", "Group Email [Required]"])
    #     google_export["Member Email"] = dusa_report["Email"]
    #     google_export["Member Type"] = "USER"
    #     google_export["Member Role"] = "MEMBER"
    #     google_export["Group Email [Required]"] = "medusa-members@medusa.org.au"
    #     if pth:
    #         google_export.to_csv(pth, index=False)
    #     return google_export