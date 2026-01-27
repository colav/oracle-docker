import os
import pickle
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload


class GoogleDriveRepository:
    SCOPES = ["https://www.googleapis.com/auth/drive"]

    def __init__(self, credentials_path: str):
        self.credentials_path = credentials_path
        self.service = self.get_service()

    def get_service(self):
        if not os.path.exists(self.credentials_path):
            raise FileNotFoundError(f"Credenciales no encontradas: {self.credentials_path}")

        with open(self.credentials_path, "rb") as token:
            creds = pickle.load(token)

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(self.credentials_path, "wb") as token:
                pickle.dump(creds, token)

        return build("drive", "v3", credentials=creds)

    def list_files(self, folder_id: str, mime_type: str | None = None):
        try:
            query = f"'{folder_id}' in parents and trashed=false"
            if mime_type:
                query += f" and mimeType='{mime_type}'"

            results = self.service.files().list(
                q=query,
                fields="files(id, name, mimeType, size, createdTime, modifiedTime)",
                pageSize=100,
                includeItemsFromAllDrives=True,
                supportsAllDrives=True
            ).execute()

            return results.get("files", [])

        except HttpError as error:
            print(f"Error listando archivos: {error}")
            return []

    def download(self, file_id: str, dest: str):
        try:
            request = self.service.files().get_media(fileId=file_id)

            with open(dest, "wb") as f:
                downloader = MediaIoBaseDownload(f, request)

                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    if status:
                        print(f"{int(status.progress() * 100)}%...", end="", flush=True)

        except HttpError as error:
            print(f"Error descargando archivo: {error}")
            raise