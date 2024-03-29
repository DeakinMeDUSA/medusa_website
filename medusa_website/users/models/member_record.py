from datetime import datetime
from itertools import islice
from time import sleep

import openpyxl
import pandas as pd
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.db.models import CharField, EmailField, ManyToManyField

from medusa_website.utils.general import chunks, get_pretty_logger

logger = get_pretty_logger(__name__)


class MemberRecord(models.Model):
    email = EmailField(primary_key=True, unique=True)
    name = CharField(blank=True, null=True, max_length=256)
    end_date = models.DateField("End date")
    import_date = models.DateField(auto_now_add=True)
    is_welcome_email_sent = models.BooleanField(default=False)
    date_welcome_email_sent = models.DateField(null=True, blank=True)

    def __repr__(self):
        return f"<MemberRecord - {self.email} - {self.name}>"

    def __str__(self):
        return f"{self.email} - {self.name}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.email = self.email.lower()
        super(MemberRecord, self).save()

    def send_welcome_email(self):
        if self.is_welcome_email_sent is True:
            raise Warning("Welcome email already sent!")

        msg = self.gen_welcome_email()
        msg.send()
        self.marked_welcome_email_sent()

    def marked_welcome_email_sent(self):
        self.is_welcome_email_sent = True
        self.date_welcome_email_sent = datetime.today().date()
        self.save()

    def gen_welcome_email(self):
        message = (
            f"Dear {self.name},\n\n"
            f"Thank you for signing up for MeDUSA.\n\n"
            f"Please complete your registration by signing up for the MeDUSA Website here: "
            f"https://www.medusa.org.au/accounts/signup/\n\n"
            f"Registering will give you access to the MCQ Bank, OSCE Bank and generate your MeDUSA ID number "
            f"which will give you MeDUSA discounts for event tickets.\n\n"
            f"Additionally our 1st year Survival Guide can be found here: https://www.medusa.org.au/publications/\n\n"
            f"Kind regards,\n\n"
            f"The MeDUSA team."
        )

        msg = EmailMultiAlternatives(
            subject="Welcome to MeDUSA",
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[self.email],
            bcc=None,
            reply_to=["contact@medusa.org.au"],
        )
        return msg

    @property
    def is_expired(self) -> bool:
        return datetime.today().date() >= self.end_date

    @property
    def has_members_record_import(self):
        return True if self.member_record_imports.all().count() > 0 else False

    @property
    def exists_as_user(self) -> bool:
        from medusa_website.users.models import User

        try:
            if User.objects.get(member_record=self):
                return True
            if User.objects.get(email=self.email):
                u = User.objects.get(email=self.email)
                u.member_record = self
                u.save()
                return True
        except User.DoesNotExist:
            return False

    @classmethod
    def send_welcome_emails_to_all_required(cls):
        welcome_emails_and_members = []  # Will be a list of tuples of (Member, EmailMsg)

        unsent_members = cls.objects.filter(is_welcome_email_sent=False)
        for member in unsent_members:
            if not member.exists_as_user and not member.is_expired:
                welcome_emails_and_members.append((member, member.gen_welcome_email()))
        if len(welcome_emails_and_members) > 0:
            from django.core import mail

            logger.info(f"Sending {len(welcome_emails_and_members)} Welcome emails")

            connection = mail.get_connection()  # Use default email connection
            emails_sent = ""
            for batch in chunks(welcome_emails_and_members, settings.EMAIL_API_MAX_BATCH_SIZE):
                emails_to_send = [msg for (member, msg) in batch]
                members_emailed = [member for (member, msg) in batch]

                emails_sent += "\n".join([msg.to[0] for msg in emails_to_send])
                if settings.DEBUG:
                    logger.warning(
                        f"DID NOT SEND MESSAGES OR MARK AS SENT, msgs would be sent to"
                        + "\n".join([msg.to[0] for msg in emails_to_send])
                    )
                else:
                    connection.send_messages(emails_to_send)

                    for member in members_emailed:
                        member.marked_welcome_email_sent()
                    sleep(1)

            notification_body = f"Sent {len(welcome_emails_and_members)} emails to:\n" f"{emails_sent}"
            notification_msg = EmailMultiAlternatives(
                subject="Welcome Email Notification",
                body=notification_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=["it@medusa.org.au"],
                bcc=None,
                reply_to=["it@medusa.org.au"],
            )
            notification_msg.send()
            logger.info(f"Sending emails successfully")
        else:
            logger.info(f"No welcome emails to send!")


class MemberRecordsImport(models.Model):
    """Represents a membership record from the DUSA exports"""

    members = ManyToManyField(MemberRecord, blank=True, related_name="member_record_imports")
    import_dt = models.DateTimeField("Import time", auto_now_add=True)
    report_date = models.DateField(help_text="Date the report was generated", unique=True)
    file = models.FileField(upload_to="dusa_reports/%Y", null=True, blank=True)

    def import_memberlist(self) -> pd.DataFrame:
        logger.info(f"Starting import of memberlist...")
        memberlist_excel = openpyxl.load_workbook(self.file.path)
        memberlist_sheet = memberlist_excel["Report"]
        data = memberlist_sheet.values
        cols = next(data)[0:]
        data = list(data)
        data = (islice(r, 0, None) for r in data)
        df = pd.DataFrame(data, index=None, columns=cols)
        logger.info(f"df = {df}")
        welcome_emails_to_send = []
        for idx, row in df.iterrows():
            member, created = MemberRecord.objects.update_or_create(
                email=row["Email"],
                defaults={"email": row["Email"], "name": row["Full Name"], "end_date": row["End Date"]},
            )
            member.member_record_imports.add(self)
            member.save()
            if created:
                member.send_welcome_email()
        logger.info(f"Finished import of member list!")
        MemberRecord.send_welcome_emails_to_all_required()

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
