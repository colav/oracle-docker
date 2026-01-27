from pathlib import Path
from drive.drive_repository import GoogleDriveRepository

class DriveService:
    def __init__(self, credentials_path: str):
        self.repo = GoogleDriveRepository(credentials_path)

    def get_folders(self, parent_id: str):
        return self.repo.list_files(
            folder_id=parent_id,
            mime_type="application/vnd.google-apps.folder"
        )

    def get_files(self, folder_id: str):
        """Obtiene archivos con metadatos incluyendo fecha de creación."""
        return self.repo.list_files(folder_id)

    def download_file(self, file_id: str, dest: Path):
        dest.parent.mkdir(parents=True, exist_ok=True)
        self.repo.download(file_id, str(dest))