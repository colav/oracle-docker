import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS", "")
    GOOGLE_PARENT_ID = os.getenv("GOOGLE_PARENT_ID", "")

    BASE_DUMP = Path.home() / "dump"
    BASE_DUMP.mkdir(exist_ok=True)

settings = Settings()
