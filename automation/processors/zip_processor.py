import zipfile
from pathlib import Path

class ZipProcessor:
    @staticmethod
    def unzip(zip_path: Path, extract_to: Path):
        if zip_path.suffix != ".zip":
            return None

        with zipfile.ZipFile(zip_path, "r") as zip:
            zip.extractall(extract_to)

        print(f"📦 Extraído: {extract_to}")
        return extract_to
