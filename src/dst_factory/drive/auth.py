from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


class GoogleDriveAuthenticator:

    SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

    def __init__(self, credentials_path: str = "credentials.json", token_path: str = "token.json",) -> None:
        self.credentials_path = Path(credentials_path)
        self.token_path = Path(token_path)


    def authenticate(self) -> Credentials:
        credentials = self._load_existing_credentials()

        if not credentials or not credentials.valid:
            credentials = self._refresh_or_login(credentials)
            self._save_credentials(credentials)

        return credentials
    
    def _load_existing_credentials(self) -> Credentials | None:
        if not self.token_path.exists():
            return None
        
        return Credentials.from_authorized_user_file(
            self.token_path, 
            self.SCOPES
        )
    
    def _refresh_or_login(self, credentials: Credentials | None) -> Credentials:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
            return credentials
        
        if not self.credentials_path.exists():
            raise FileNotFoundError(f"Credentials file not found at {self.credentials_path}")
        
        flow = InstalledAppFlow.from_client_secrets_file(
            self.credentials_path, 
            self.SCOPES
        )

        credentials = flow.run_local_server(port=0)

        return credentials
    

    def _save_credentials(self, credentials: Credentials) -> None:
        self.token_path.write_text(
            credentials.to_json(),
            encoding="utf-8"
        )
