import sys
from pathlib import Path
import urllib.request
import json
import traceback

backend_dir = Path(__file__).parent.resolve()
sys.path.insert(0, str(backend_dir))

from app.services.email_service import EmailSender

try:
    print("Testing EmailSender with bhoomicase07@gmail.com credentials...")
    result = EmailSender.send_verification_email(
        email="projectdevsecops1405@gmail.com",
        first_name="TestRender",
        verification_token="test-token",
        base_url="https://bhoomi-case.onrender.com"
    )
    print(f"Result: {result}")
except Exception as e:
    print(f"Exception: {e}")
    traceback.print_exc()
