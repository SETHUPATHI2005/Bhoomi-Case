"""
FastAPI dependency injection factories shared across routers.
"""
import logging
from typing import Optional

from fastapi import Header, HTTPException

from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger("dependencies")


def verify_admin(
    authorization: Optional[str] = Header(None)
) -> str:
    """Verify admin using session token from the token store."""
    from app.services.user_service import load_tokens, verify_user_token

    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:]

    if not token:
        raise HTTPException(status_code=401, detail="Missing authorization token")

    # First check the token store directly for admin username
    tokens = load_tokens()
    token_entry = next((t for t in tokens if t.get("token") == token), None)
    
    if not token_entry:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    username = token_entry.get("username")
    if username != settings.admin_username:
        raise HTTPException(status_code=403, detail="Principal is not an authorized administrator")

    return username



def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    """Verify user session token.
    
    Returns the user dict on success.
    Raises HTTP 401 on failure.
    """
    from app.services.user_service import verify_user_token
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:]
    
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
        
    user = verify_user_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
        
    return user
