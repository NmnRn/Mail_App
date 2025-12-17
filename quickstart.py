import os
import base64
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.readonly",
]

TOKEN_DIR = "Tokens"
TOKEN_PATH = os.path.join(TOKEN_DIR, "token.json")
CREDS_PATH = "credentials.json"

_creds = None


def ensure_credentials():
    """
    Ensures OAuth credentials exist and are valid.
    Creates/refreshes Tokens/token.json when needed.
    """
    global _creds

    if _creds and _creds.valid:
        return _creds

    os.makedirs(TOKEN_DIR, exist_ok=True)

    if os.path.exists(TOKEN_PATH):
        _creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not _creds or not _creds.valid:
        if _creds and _creds.expired and _creds.refresh_token:
            _creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
            _creds = flow.run_local_server(port=0)

        with open(TOKEN_PATH, "w", encoding="utf-8") as token_file:
            token_file.write(_creds.to_json())

    return _creds


def gmail_send_message(to: str, subject: str, content: str) -> bool:
    """
    Sends an email using Gmail API.
    Returns True on success, False on failure.
    """
    try:
        creds = ensure_credentials()
        service = build("gmail", "v1", credentials=creds)

        message = EmailMessage()
        message.set_content(content)
        message["To"] = to
        message["Subject"] = subject

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
        body = {"raw": encoded_message}

        service.users().messages().send(userId="me", body=body).execute()
        return True

    except HttpError as error:
        print(f"Gmail API error (send): {error}")
        return False


def _get_header(headers: list[dict], name: str) -> str:
    name = name.lower()
    for h in headers:
        if h.get("name", "").lower() == name:
            return h.get("value", "")
    return ""


def get_mails(limit: int = 20) -> list[dict]:
    """
    Fetches latest inbox emails (metadata only) and returns a list of dicts:
    [
      {"id","from","subject","date","snippet"},
      ...
    ]
    """
    try:
        creds = ensure_credentials()
        service = build("gmail", "v1", credentials=creds)

        res = service.users().messages().list(
            userId="me",
            labelIds=["INBOX"],
            maxResults=limit,
        ).execute()

        items = res.get("messages", [])
        out: list[dict] = []

        for item in items:
            m = service.users().messages().get(
                userId="me",
                id=item["id"],
                format="metadata",
                metadataHeaders=["From", "Subject", "Date"],
            ).execute()

            headers = m.get("payload", {}).get("headers", [])
            out.append({
                "id": m.get("id", ""),
                "from": _get_header(headers, "From"),
                "subject": _get_header(headers, "Subject") or "(No subject)",
                "date": _get_header(headers, "Date"),
                "snippet": m.get("snippet", ""),
            })

        return out

    except HttpError as error:
        print(f"Gmail API error (list/get): {error}")
        return []


if __name__ == "__main__":
    # Manual test (run: python quickstart.py)
    # IMPORTANT: Do not commit credentials.json or Tokens/token.json to GitHub.
    ensure_credentials()
    mails = get_mails(limit=20)

