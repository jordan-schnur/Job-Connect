import os.path
import base64
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from Config import Configuration

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.compose", "https://www.googleapis.com/auth/gmail.modify"]


def create_message(sender, to, subject, message_text):
    """Create a MIMEText message."""
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message}


def create_draft(service, user_id, message_body):
    """Create a draft email."""
    try:
        draft = service.users().drafts().create(userId=user_id, body={'message': message_body}).execute()
        return True
    except HttpError as error:
        print(f'An error occurred: {error}')
        raise error


def service_login():
    """Login to the Gmail API and return the service."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)
    return service


class Gmail:
    def __init__(self):
        self.service = service_login()

    def send_email(self, config: Configuration, to, subject: str, message_text: str):
        message_body = create_message(config.user.email, to, subject, message_text)
        create_draft(self.service, "me", message_body)
