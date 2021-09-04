import io
from typing import Dict

from django.conf import settings
from django.core.files import File
from tqdm import tqdm

from medusa_website import celery_app as app
from medusa_website.gmailapi_backend.mail import GmailBackend
from medusa_website.users.models import MemberRecordsImport


@app.task
def get_and_import_latest_memberlist_report():
    gmail = GmailBackend(account_email=settings.MEMBERLIST_EMAIL)
    members_report_emails = gmail.get_messages(subject="Report: Club members weekly report", latest_first=True)
    latest_report = members_report_emails[0]
    new_import = get_and_import_memberlist(gmail, latest_report)
    print(f"Successfully imported and wrote latest member report to {new_import.file.path}")


@app.task
def get_and_import_all_memberlists():
    gmail = GmailBackend(account_email=settings.MEMBERLIST_EMAIL)
    members_report_emails = gmail.get_messages(subject="Report: Club members weekly report", latest_first=True)
    for members_report_email in tqdm(members_report_emails):
        get_and_import_memberlist(gmail, members_report_email)


@app.task
def get_and_import_memberlist(gmail: GmailBackend, members_report_email: Dict) -> MemberRecordsImport:
    members_report_data, attach_fname = gmail.get_attachment_for_message(members_report_email)
    report_date = gmail.get_date_of_msg(members_report_email).date()
    report_fname = f"{attach_fname.stem}_{report_date.isoformat()}{attach_fname.suffix}"

    try:
        existing_report = MemberRecordsImport.objects.get(report_date=report_date)
        print(f"Report for data {report_date.isoformat()} already exists!")
        return existing_report
    except MemberRecordsImport.DoesNotExist:
        with io.BytesIO() as b:
            b.write(members_report_data)
            temp_report = File(b, name=report_fname)
            new_import = MemberRecordsImport(file=temp_report, report_date=report_date)
            new_import.save()
            new_import.import_memberlist()
        return new_import
