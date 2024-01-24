import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials


SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def get_credentials() -> None | Credentials:
    if os.path.exists("credentials.json"):
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
        return Credentials.from_authorized_user_file("token.json", SCOPES)
    else:
        print("Credentials were not provided")
