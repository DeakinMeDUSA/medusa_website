"""
Email backend that uses the GMail API via OAuth2 authentication.
"""
import base64
import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple

import dateparser
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

from medusa_website.utils.general import get_pretty_logger

logger = get_pretty_logger(__name__)


class GmailBackend(BaseEmailBackend):
    SCOPES = settings.GMAIL_SCOPES
    CREDS_PTH = settings.GMAIL_CREDENTIALS_PATH

    def __init__(self, account_email: str = None, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently, **kwargs)

        self.account_email = account_email or settings.DEFAULT_FROM_EMAIL
        self.credentials = self.authenticate(self.account_email)
        self.user_id = "me"
        self.service = build("gmail", "v1", credentials=self.credentials, cache_discovery=False)

    def authenticate(self, account_email: str) -> Credentials:
        def refresh_cred(cred: Credentials):
            if cred.valid is False:
                cred.refresh(Request())
                print(f"Refreshed credentials for {cred.signer_email}")

        service_credentials = Credentials.from_service_account_file(str(self.CREDS_PTH), scopes=self.SCOPES)
        refresh_cred(service_credentials)

        print(f"Getting user credentials for {account_email} ...")
        user_credentials = service_credentials.with_subject(account_email)
        refresh_cred(user_credentials)

        return user_credentials

    def send_message(self, email_message):
        if not email_message.recipients():
            return False
        raw_message = {"raw": base64.urlsafe_b64encode(email_message.message().as_bytes()).decode()}
        return self.service.users().messages().send(userId=self.user_id, body=raw_message)

    def send_messages(self, email_messages):
        """Send all messages using BatchHttpRequest"""
        if not email_messages:
            return 0
        msg_count = 0
        last_exception = None

        def send_callback(r_id, response, exception):
            nonlocal msg_count, last_exception
            if exception is not None:
                logger.exception("An error occurred sending the message via GMail API:  %s", exception)
                last_exception = exception
            else:
                msg_count += 1

        batch = self.service.new_batch_http_request(send_callback)
        for message in email_messages:
            batch.add(self.send_message(message))
        batch.execute()
        if not self.fail_silently and last_exception:
            raise last_exception
        return msg_count

    def get_email(self, subject: str, latest=True):
        raise NotImplementedError()

    def get_messages(self, subject: str, latest_first=True):
        def get_items(request_id, response, exception):
            if exception is not None:
                print(f"An error occurred for request_id {request_id}: {exception}")
            else:
                returned_messages.extend(response["messages"])

        returned_messages = []

        query = f""
        if subject:
            query += f"subject:{subject} "

        print(f"Getting messages with query:\n{query}")
        results = self.service.users().messages().list(userId="me", q=query).execute()
        messages_inital = results["messages"]

        if messages_inital != []:
            batch = self.service.new_batch_http_request(callback=get_items)
            batch._batch_uri = "https://www.googleapis.com/batch/gmail/v1"

            for msg in messages_inital:
                batch.add(self.service.users().threads().get(userId="me", id=msg["id"]))

            batch.execute()
        else:
            raise RuntimeError(f"No messages found with query: {query}")

        if latest_first:
            returned_messages.sort(key=lambda m: m["internalDate"], reverse=True)
        return returned_messages

    def get_attachment_for_message(self, msg: Dict) -> Tuple[Optional[bytes], Optional[Path]]:
        for part in msg["payload"]["parts"]:
            if part["filename"]:
                attachment_id = part["body"]["attachmentId"]
                # try:
                print(f"attachment_id = {attachment_id}")
                attachment = (
                    self.service.users()
                    .messages()
                    .attachments()
                    .get(userId="me", messageId=msg["id"], id=attachment_id)
                    .execute()
                )
                file_data = base64.urlsafe_b64decode(attachment["data"].encode("UTF-8"))
                return file_data, Path(part["filename"])
        else:
            return None, None

    @staticmethod
    def get_date_of_msg(msg) -> datetime.datetime:
        for header in msg["payload"]["headers"]:
            if header["name"] == "Date":
                return dateparser.parse(header["value"].replace(" (UTC)", ""))
        else:  # no-return
            raise RuntimeError(f"Could not find date for msg id {msg['id']}")
