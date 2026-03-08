"""Authentication router — /api/v1/auth/* endpoints."""
import json
import logging
from datetime import datetime
from typing import Optional
from urllib.parse import parse_qs

from fastapi import APIRouter, Header, HTTPException, Request
from fastapi.responses import JSONResponse

from app.services.email_service import EmailSender, EmailToken
from app.services.user_service import (
    create_demo_user,
    find_user_by_email,
    find_user_by_username,
    generate_token,
    hash_password,
    load_tokens,
    load_users,
    save_tokens,
    save_users,
    verify_user_token,
    update_user_profile,
)

from app.core.config import get_settings

router = APIRouter(tags=["auth"])
logger = logging.getLogger("router.auth")

@router.get("/email-config-status")
async def get_email_config_status():
    """Diagnostic endpoint to check if email environment variables are loaded (safely)."""
    settings = get_settings()
    return JSONResponse(content={
        "status": "ok",
        "email_enabled": settings.enable_email,
        "smtp_server_configured": bool(settings.smtp_server),
        "smtp_server": settings.smtp_server,
        "smtp_port": settings.smtp_port,
        "smtp_user_configured": bool(settings.smtp_user),
        "smtp_user_preview": settings.smtp_user[:4] + "***" if settings.smtp_user else None,
        "smtp_password_configured": bool(settings.smtp_password),
        "sender_email": settings.sender_email
    })

def _get_base_url(request: Request) -> str:
    return str(request.base_url).rstrip("/")


# ── Register ──────────────────────────────────────────────────────────────────

@router.post("/register", status_code=201)
async def register(request: Request):
    """Register a new user account."""
    try:
        payload = await request.json()

        username = str(payload.get("username", "")).strip()
        email = str(payload.get("email", "")).strip()
        password = str(payload.get("password", ""))
        first_name = str(payload.get("first_name", "")).strip()
        last_name = str(payload.get("last_name", "")).strip()
        contact_number = str(payload.get("contact_number", "")).strip()
        user_type = payload.get("user_type", "citizen")

        if not all([username, email, password, first_name]):
            raise HTTPException(status_code=400, detail="Missing required fields")
        if not (4 <= len(username) <= 20):
            raise HTTPException(status_code=400, detail="Username must be 4–20 characters")
        if len(password) < 6:
            raise HTTPException(status_code=400, detail="Password must be 6+ characters")
        if not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
            raise HTTPException(status_code=400, detail="Password must contain letters and numbers")
        if contact_number and (not contact_number.isdigit() or len(contact_number) != 10):
            raise HTTPException(status_code=400, detail="Contact number must be exactly 10 digits")
        if find_user_by_username(username):
            raise HTTPException(status_code=409, detail="Username already exists")
        if find_user_by_email(email):
            raise HTTPException(status_code=409, detail="Email already registered")

        now = datetime.now().isoformat()
        new_user = {
            "username": username,
            "password": hash_password(password),
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "contact_number": contact_number,
            "user_type": user_type,
            "created_at": now,
            "updated_at": now,
            "email_verified": False,
            "email_verified_at": None,
            "verified": False,
            "verified_at": None,
            "verified_by": None,
        }
        users = load_users()
        users.append(new_user)
        save_users(users)

        verification_token = EmailToken.generate_token(email, token_type="verify")
        email_sent = False
        try:
            email_sent = EmailSender.send_verification_email(
                email, first_name, verification_token, base_url=_get_base_url(request)
            )
        except Exception as email_err:
            logger.error(f"Email sending exception for {username}: {email_err}")

        if not email_sent:
            logger.warning(f"Verification email not sent for: {username} — user can resend later")

        logger.info(f"New user registered: {username} ({user_type})")
        msg = (
            "User registered successfully. Please check your email to verify your account."
            if email_sent
            else "Account created successfully! Please use 'Resend Verification Email' to get your verification link."
        )
        return JSONResponse(
            status_code=201,
            content={
                "status": "ok",
                "message": msg,
                "email_sent": email_sent,
                "user": {
                    "username": username,
                    "email": email,
                    "first_name": first_name,
                    "user_type": user_type,
                    "contact_number": contact_number,
                },
            },
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(status_code=500, detail="Registration failed")


# ── Login ─────────────────────────────────────────────────────────────────────

@router.post("/login")
async def login(request: Request):
    """Login and receive a session token."""
    try:
        payload = await request.json()
        username = str(payload.get("username", "")).strip()
        password = str(payload.get("password", ""))

        if not username or not password:
            raise HTTPException(status_code=400, detail="Username and password required")

        user = find_user_by_username(username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not user.get("email_verified", False):
            raise HTTPException(
                status_code=403,
                detail="Email not verified. Please check your email to verify your account.",
            )

        if user.get("password") != hash_password(password):
            raise HTTPException(status_code=401, detail="Invalid password")

        token = generate_token()
        tokens = load_tokens()
        tokens.append({"token": token, "username": username, "created_at": datetime.now().isoformat()})
        save_tokens(tokens)

        logger.info(f"User logged in: {username}")
        return JSONResponse(content={
            "status": "ok",
            "token": token,
            "user": {
                "username": user.get("username"),
                "email": user.get("email"),
                "first_name": user.get("first_name"),
                "last_name": user.get("last_name"),
                "contact_number": user.get("contact_number", ""),
                "user_type": user.get("user_type"),
                "created_at": user.get("created_at"),
            },
        })
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail="Login failed")


@router.post("/admin-login")
async def admin_login(request: Request):
    """Secure login for administrators."""
    try:
        payload = await request.json()
        username = str(payload.get("username", "")).strip()
        password = str(payload.get("password", ""))

        from app.core.config import get_settings
        settings = get_settings()

        if (username == settings.admin_username and 
            password == settings.admin_password):
            
            # Generate session token and save it (same flow as regular login)
            token = generate_token()
            tokens = load_tokens()
            tokens.append({"token": token, "username": username, "created_at": datetime.now().isoformat()})
            save_tokens(tokens)

            logger.info(f"Admin logged in successfully: {username}")
            return JSONResponse(content={
                "status": "ok",
                "token": token,
                "message": "Admin authenticated",
                "user": {
                    "username": username,
                    "user_type": "admin"
                }
            })
        
        logger.warning(f"Failed admin login attempt for: {username}")
        raise HTTPException(status_code=401, detail="Invalid admin credentials")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Admin login error: {e}")
        raise HTTPException(status_code=500, detail="Admin login failed")



# ── Profile ───────────────────────────────────────────────────────────────────

@router.get("/profile")
async def get_profile(authorization: Optional[str] = Header(None)):
    """Return authenticated user's profile (no password)."""
    try:
        token = None
        if authorization and authorization.startswith("Bearer "):
            token = authorization[7:]
        if not token:
            raise HTTPException(status_code=401, detail="Missing token")

        user = verify_user_token(token)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        return JSONResponse(content={k: v for k, v in user.items() if k != "password"})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Profile fetch error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch profile")


@router.patch("/profile")
async def update_profile(request: Request, authorization: Optional[str] = Header(None)):
    """Update authenticated user's profile."""
    try:
        token = None
        if authorization and authorization.startswith("Bearer "):
            token = authorization[7:]
        if not token:
            raise HTTPException(status_code=401, detail="Missing token")

        user = verify_user_token(token)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        payload = await request.json()
        updated_user = update_user_profile(user["username"], payload)
        
        if not updated_user:
            raise HTTPException(status_code=400, detail="Failed to update profile. Email might be already in use.")

        logger.info(f"Profile updated for: {user['username']}")
        return JSONResponse(content={
            "status": "ok", 
            "message": "Profile updated successfully",
            "user": {k: v for k, v in updated_user.items() if k != "password"}
        })
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Profile update error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update profile")


# ── Logout ────────────────────────────────────────────────────────────────────

@router.post("/logout")
async def logout(authorization: Optional[str] = Header(None)):
    """Invalidate the current session token."""
    try:
        token = None
        if authorization and authorization.startswith("Bearer "):
            token = authorization[7:]
        if token:
            tokens = [t for t in load_tokens() if t.get("token") != token]
            save_tokens(tokens)
        return JSONResponse(content={"status": "ok", "message": "Logged out successfully"})
    except Exception as e:
        logger.error(f"Logout error: {e}")
        raise HTTPException(status_code=500, detail="Logout failed")


# ── Email Verification ────────────────────────────────────────────────────────

@router.post("/verify-email")
async def verify_email(request: Request):
    """Verify user email with a token from the verification link."""
    try:
        payload = await request.json()
        token = str(payload.get("token", "")).strip()
        if not token:
            raise HTTPException(status_code=400, detail="Verification token required")

        email = EmailToken.verify_token(token, token_type="verify")
        if not email:
            raise HTTPException(status_code=400, detail="Invalid or expired verification token")

        users = load_users()
        idx = next((i for i, u in enumerate(users) if u.get("email") == email), None)
        if idx is None:
            raise HTTPException(status_code=404, detail="User not found")

        users[idx]["email_verified"] = True
        users[idx]["email_verified_at"] = datetime.now().isoformat()
        save_users(users)
        EmailToken.mark_token_used(token)

        logger.info(f"Email verified for: {users[idx].get('username')}")
        return JSONResponse(content={"status": "ok", "message": "Email verified successfully. You can now login."})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Email verification error: {e}")
        raise HTTPException(status_code=500, detail="Email verification failed")


@router.post("/resend-verification-email")
async def resend_verification_email(request: Request):
    """Resend the email verification link."""
    try:
        payload = await request.json()
        email = str(payload.get("email", "")).strip()
        if not email:
            raise HTTPException(status_code=400, detail="Email address required")

        user = find_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.get("email_verified", False):
            raise HTTPException(status_code=400, detail="Email already verified")

        token = EmailToken.generate_token(email, token_type="verify")
        sent = EmailSender.send_verification_email(
            email, user.get("first_name", "User"), token, base_url=_get_base_url(request)
        )
        if not sent:
            raise HTTPException(status_code=503, detail="Failed to send verification email. Please try again.")

        return JSONResponse(content={"status": "ok", "message": "Verification email sent successfully"})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Resend verification error: {e}")
        raise HTTPException(status_code=500, detail="Failed to resend verification email")


# ── Password Reset ────────────────────────────────────────────────────────────

@router.post("/request-password-reset")
async def request_password_reset(request: Request):
    """Initiate password reset — sends email if account exists."""
    try:
        email = ""
        content_type = request.headers.get("content-type", "").lower()
        if "application/json" in content_type:
            try:
                payload = await request.json()
                email = str(payload.get("email", "")).strip()
            except json.JSONDecodeError:
                raw = (await request.body()).decode("utf-8", errors="ignore")
                email = str(parse_qs(raw).get("email", [""])[0]).strip()
        else:
            raw = (await request.body()).decode("utf-8", errors="ignore")
            email = str(parse_qs(raw).get("email", [""])[0]).strip()

        if not email:
            raise HTTPException(status_code=400, detail="Email address required")

        user = find_user_by_email(email)
        neutral = {"status": "ok", "message": "If email exists, password reset link has been sent"}
        if not user:
            return JSONResponse(content=neutral)

        try:
            reset_token = EmailToken.generate_token(email, token_type="reset")
            sent = EmailSender.send_password_reset_email(
                email, user.get("first_name", "User"), reset_token, base_url=_get_base_url(request)
            )
            if not sent:
                logger.error(f"Failed to send password reset email to: {email}")
        except Exception as mail_err:
            logger.error(f"Password reset email workflow failed for {email}: {mail_err}")

        logger.info(f"Password reset requested for: {email}")
        return JSONResponse(content=neutral)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Password reset request error: {e}")
        raise HTTPException(status_code=500, detail="Failed to process password reset request")


@router.post("/reset-password")
async def reset_password(request: Request):
    """Reset password using a valid reset token."""
    try:
        payload = await request.json()
        token = str(payload.get("token", "")).strip()
        new_password = str(payload.get("password", ""))

        if not token or not new_password:
            raise HTTPException(status_code=400, detail="Token and new password required")
        if len(new_password) < 6:
            raise HTTPException(status_code=400, detail="Password must be 6+ characters")
        if not any(c.isalpha() for c in new_password) or not any(c.isdigit() for c in new_password):
            raise HTTPException(status_code=400, detail="Password must contain letters and numbers")

        email = EmailToken.verify_token(token, token_type="reset")
        if not email:
            raise HTTPException(status_code=400, detail="Invalid or expired reset token")

        users = load_users()
        idx = next((i for i, u in enumerate(users) if u.get("email") == email), None)
        if idx is None:
            raise HTTPException(status_code=404, detail="User not found")

        users[idx]["password"] = hash_password(new_password)
        users[idx]["password_reset_at"] = datetime.now().isoformat()
        save_users(users)
        EmailToken.mark_token_used(token)

        logger.info(f"Password reset for: {users[idx].get('username')}")
        return JSONResponse(content={"status": "ok", "message": "Password reset successfully. You can now login."})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Password reset error: {e}")
        raise HTTPException(status_code=500, detail="Password reset failed")
