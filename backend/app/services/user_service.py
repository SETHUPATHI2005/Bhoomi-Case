"""User service: all user data access and business-logic helpers."""
import hashlib
import json
import logging
import pathlib
import secrets
from datetime import datetime
from typing import Optional

logger = logging.getLogger("user_service")

BASE_DIR = pathlib.Path(__file__).resolve().parents[1]  # → backend/app/
USERS_FILE = BASE_DIR / "data" / "users.json"
TOKENS_FILE = BASE_DIR / "data" / "user_tokens.json"


# ── Helpers ──────────────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def generate_token() -> str:
    """Generate a cryptographically secure URL-safe token."""
    return secrets.token_urlsafe(32)


# ── Users persistence ─────────────────────────────────────────────────────────

def load_users() -> list:
    """Load all users from JSON store."""
    try:
        if USERS_FILE.exists():
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Error loading users: {e}")
    return []


def save_users(users: list) -> None:
    """Persist user list to JSON store."""
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


# ── Tokens persistence ────────────────────────────────────────────────────────

def load_tokens() -> list:
    """Load all session tokens from JSON store."""
    try:
        if TOKENS_FILE.exists():
            with open(TOKENS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Error loading tokens: {e}")
    return []


def save_tokens(tokens: list) -> None:
    """Persist session tokens to JSON store."""
    TOKENS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TOKENS_FILE, "w", encoding="utf-8") as f:
        json.dump(tokens, f, ensure_ascii=False, indent=2)


# ── Lookup helpers ────────────────────────────────────────────────────────────

def find_user_by_username(username: str) -> Optional[dict]:
    """Return user dict matching username, or None."""
    return next((u for u in load_users() if u.get("username") == username), None)


def find_user_by_email(email: str) -> Optional[dict]:
    """Return user dict matching email, or None."""
    return next((u for u in load_users() if u.get("email") == email), None)


def verify_user_token(token: str) -> Optional[dict]:
    """Verify a session token and return the associated user dict."""
    for entry in load_tokens():
        if entry.get("token") == token:
            return find_user_by_username(entry.get("username"))
    return None


def update_user_profile(username: str, updates: dict) -> Optional[dict]:
    """Update user profile fields and persist changes."""
    users = load_users()
    for i, user in enumerate(users):
        if user.get("username") == username:
            # Fields allowed to be updated
            allowed_fields = {"first_name", "last_name", "email", "contact_number"}
            
            # Check if email is being changed and if it already exists
            new_email = updates.get("email")
            if new_email and new_email != user.get("email"):
                if any(u.get("email") == new_email for u in users if u.get("username") != username):
                    return None  # Email already taken
            
            # Apply updates
            for field in allowed_fields:
                if field in updates:
                    user[field] = str(updates[field]).strip()

            contact_number = user.get("contact_number", "")
            if contact_number and (not contact_number.isdigit() or len(contact_number) != 10):
                return None
            
            user["updated_at"] = datetime.now().isoformat()
            users[i] = user
            save_users(users)
            return user
    return None


# ── Initialisation ────────────────────────────────────────────────────────────

def create_demo_user() -> None:
    """Ensure a demo user account exists (for development)."""
    users = load_users()
    if not any(u.get("username") == "demo" for u in users):
        now = datetime.now().isoformat()
        users.append({
            "username": "demo",
            "password": hash_password("demo123"),
            "email": "demo@bhoomi.local",
            "first_name": "Demo",
            "last_name": "User",
            "contact_number": "",
            "user_type": "citizen",
            "created_at": now,
            "updated_at": now,
            "email_verified": True,
            "email_verified_at": now,
            "verified": True,
            "verified_at": now,
            "verified_by": "system",
        })
        save_users(users)
        logger.info("Demo user created: demo / demo123")
