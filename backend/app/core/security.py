"""JWT-based security utilities (token creation and verification)."""
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from pydantic import BaseModel

from app.core.config import get_settings

settings = get_settings()


class TokenData(BaseModel):
    sub: str  # subject (user / admin id)
    exp: Optional[datetime] = None
    scopes: list = []


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(hours=settings.jwt_expiration_hours)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def verify_token(token: str) -> Optional[TokenData]:
    """Verify and decode a JWT token. Returns None if invalid."""
    try:
        payload = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
        sub: str = payload.get("sub")
        if sub is None:
            return None
        return TokenData(sub=sub, scopes=payload.get("scopes", []))
    except JWTError:
        return None


def create_admin_token(admin_id: str = "admin") -> str:
    """Create an admin-scoped JWT token."""
    return create_access_token({"sub": admin_id, "scopes": ["admin"]})
