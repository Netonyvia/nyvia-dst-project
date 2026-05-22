from typing import Any
from io import BytesIO

from googleapiclient.http import MediaIoBaseDownload    
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

    def list_folders(self) -> list[dict]:
        response = (self.service.files().list(q="mimeType='application/vnd.google-apps.folder' and trashed=false", 
                    pagesize=1000, fields = "files(id, name)").execute()
        )
        return response.get("files", [])
    
    def list_files_in_folder(self, folder_id: str) -> list[dict]:
        query = f"'{folder_id}' in parents and trashed=false"
        response = self.service.files().list(q=query, fields="files(id, name, mimeType)").execute()
        return response.get("files", [])
    
    def export_google_doc_As_text(self, file_id: str) -> str:
        request = self.service.files().export_media(fileId=file_id, mimeType="text/plain")
        buffer = BytesIO()
        downloader = MediaIoBaseDownload(buffer, request)

        done = False
        while not done:
            _, done = downloader.next_chunk()

        return buffer.getvalue().decode("utf-8")
    
    def download_file_bytes(self, file_id: str) -> bytes:
        request = self.service.files().get_media(fileId=file_id)

        buffer = BytesIO()
        downloader = MediaIoBaseDownload(buffer, request)

        done = False
        while not done:
            _, done = downloader.next_chunk()

        return buffer.getvalue()
    


