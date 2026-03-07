"""Case / parcel service: data access helpers for parcels and cases."""
import json
import logging
import pathlib
from typing import Optional

logger = logging.getLogger("case_service")

BASE_DIR = pathlib.Path(__file__).resolve().parents[1]  # → backend/app/
DATA_FILE = BASE_DIR / "data" / "sample_parcels.json"
ADMIN_STORE = BASE_DIR / "data" / "admin_uploads.json"


def load_data() -> list:
    """Load seed parcel data from sample_parcels.json."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading sample data: {e}")
        return []


def load_admin_uploads() -> list:
    """Load admin-uploaded parcels from admin_uploads.json."""
    try:
        if ADMIN_STORE.exists():
            with open(ADMIN_STORE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Error loading admin uploads: {e}")
    return []


def save_admin_uploads(uploads: list) -> None:
    """Persist admin-uploaded parcels."""
    ADMIN_STORE.parent.mkdir(parents=True, exist_ok=True)
    with open(ADMIN_STORE, "w", encoding="utf-8") as f:
        json.dump(uploads, f, ensure_ascii=False, indent=2)


CITIZEN_STORE = BASE_DIR / "data" / "citizen_submissions.json"

def load_citizen_submissions() -> list:
    """Load pending case submissions from citizens."""
    try:
        if CITIZEN_STORE.exists():
            with open(CITIZEN_STORE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Error loading citizen submissions: {e}")
    return []

def save_citizen_submissions(submissions: list) -> None:
    """Persist pending case submissions from citizens."""
    CITIZEN_STORE.parent.mkdir(parents=True, exist_ok=True)
    with open(CITIZEN_STORE, "w", encoding="utf-8") as f:
        json.dump(submissions, f, ensure_ascii=False, indent=2)


import shutil
import uuid

UPLOADS_DIR = BASE_DIR / "uploads"

async def save_upload_file(upload_file, sub_directory: str = "") -> Optional[str]:
    """Save an uploaded file to the uploads directory.
    
    Returns the relative path to the saved file or None if failed.
    """
    try:
        if not upload_file or not upload_file.filename:
            return None
            
        # Create submission-specific directory if provided
        target_dir = UPLOADS_DIR
        if sub_directory:
            target_dir = target_dir / sub_directory
        
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename to avoid collisions
        ext = pathlib.Path(upload_file.filename).suffix
        safe_filename = f"{uuid.uuid4().hex}{ext}"
        file_path = target_dir / safe_filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
            
        # Return relative path for static serving
        rel_path = f"/uploads/{sub_directory}/{safe_filename}" if sub_directory else f"/uploads/{safe_filename}"
        return rel_path.replace("//", "/")
    except Exception as e:
        logger.error(f"Error saving file {upload_file.filename}: {e}")
        return None


def find_case_in_parcel(case_id: str, parcels: list) -> tuple:
    """Locate a case and its parent parcel.

    Returns:
        (parcel, case, parcel_index) if found, else (None, None, None).
    """
    for idx, parcel in enumerate(parcels):
        for case in parcel.get("linked_cases", []):
            if case.get("case_id") == case_id:
                return parcel, case, idx
    return None, None, None


def normalize(s: Optional[str]) -> str:
    """Normalise a village/survey string for fuzzy matching."""
    if not s:
        return ""
    return "".join(ch for ch in s.lower() if ch.isalnum())
