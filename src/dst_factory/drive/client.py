from typing import Any

from googleapiclient.discovery import build

from dst_factory.drive.auth import GoogleDriveAuthenticator


class GoogleDriveClient:
    """Google Drive API client wrapper."""

    def __init__(self, authenticator: GoogleDriveAuthenticator | None = None) -> None:
        self.authenticator = authenticator or GoogleDriveAuthenticator()
        self._service: Any | None = None

    @property
    def service(self) -> Any:
        if self._service is None:
            credentials = self.authenticator.authenticate()
            self._service = build("drive", "v3", credentials=credentials)

        return self._service

    def authenticate(self) -> None:
        _ = self.service