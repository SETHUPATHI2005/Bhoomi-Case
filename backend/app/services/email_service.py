"""Email utility module — sends verification and password-reset emails."""

import smtplib
import logging
import json
import pathlib
import secrets
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta, timezone
from typing import Optional

from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger("email_service")

BASE_DIR = pathlib.Path(__file__).resolve().parents[1]  # → backend/app/
EMAIL_TOKENS_FILE = BASE_DIR / "data" / "email_tokens.json"


class EmailToken:
    """Manage email verification and password-reset tokens (JSON-backed store)."""

    @staticmethod
    def generate_token(email: str, token_type: str = "verify") -> str:
        """Generate and persist a secure token for the given email."""
        token = secrets.token_urlsafe(32)
        expiry_hours = (
            settings.email_verification_expiry_hours
            if token_type == "verify"
            else settings.password_reset_expiry_hours
        )
        tokens = EmailToken._load_tokens()
        tokens.append({
            "token": token,
            "email": email,
            "type": token_type,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "expires_at": (
                datetime.now(timezone.utc) + timedelta(hours=expiry_hours)
            ).isoformat(),
            "used": False,
            "used_at": None,
        })
        EmailToken._save_tokens(tokens)
        return token

    @staticmethod
    def verify_token(token: str, token_type: str = "verify") -> Optional[str]:
        """Verify token validity; return associated email or None."""
        for entry in EmailToken._load_tokens():
            if entry.get("token") == token and entry.get("type") == token_type:
                if entry.get("used"):
                    return None
                expires_at = datetime.fromisoformat(entry.get("expires_at", ""))
                if datetime.now(timezone.utc) > expires_at:
                    return None
                return entry.get("email")
        return None

    @staticmethod
    def mark_token_used(token: str) -> bool:
        """Mark a token as consumed."""
        tokens = EmailToken._load_tokens()
        for entry in tokens:
            if entry.get("token") == token:
                entry["used"] = True
                entry["used_at"] = datetime.now(timezone.utc).isoformat()
                EmailToken._save_tokens(tokens)
                return True
        return False

    @staticmethod
    def _load_tokens() -> list:
        try:
            if EMAIL_TOKENS_FILE.exists():
                with open(EMAIL_TOKENS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
        return []

    @staticmethod
    def _save_tokens(tokens: list) -> None:
        EMAIL_TOKENS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(EMAIL_TOKENS_FILE, "w", encoding="utf-8") as f:
            json.dump(tokens, f, ensure_ascii=False, indent=2)


class EmailSender:
    """Send transactional emails via SMTP."""

    @staticmethod
    def send_verification_email(
        email: str,
        first_name: str,
        verification_token: str,
        base_url: str = "http://localhost:8000",
    ) -> bool:
        if not settings.enable_email:
            logger.warning(f"Email disabled — skipping verification email for {email}")
            return True
        try:
            link = f"{base_url}/static/verify-email.html?token={verification_token}"
            subject = "Verify Your Bhoomi Account — Action Required"
            html = f"""
            <html><body style="font-family:Arial,sans-serif;color:#333">
              <div style="max-width:600px;margin:0 auto;padding:20px">
                <h2 style="color:#2c3e50">Welcome to Bhoomi, {first_name}!</h2>
                <p>Please verify your email address to activate your account.</p>
                <p><a href="{link}" style="display:inline-block;padding:10px 20px;background:#3498db;color:#fff;text-decoration:none;border-radius:5px">Verify Email</a></p>
                <p>Or copy this link: <code>{link}</code></p>
                <p style="color:#7f8c8d;font-size:12px">This link expires in 24 hours.</p>
                <hr><p style="color:#7f8c8d;font-size:12px">If you didn't create this account, ignore this email.</p>
              </div>
            </body></html>"""
            return EmailSender._send_email(email, subject, html)
        except Exception as e:
            logger.error(f"Error sending verification email: {e}")
            return False

    @staticmethod
    def send_password_reset_email(
        email: str,
        first_name: str,
        reset_token: str,
        base_url: str = "http://localhost:8000",
    ) -> bool:
        if not settings.enable_email:
            logger.warning(f"Email disabled — skipping password reset email for {email}")
            return True
        try:
            link = f"{base_url}/static/reset-password.html?token={reset_token}"
            subject = "Password Reset Request — Bhoomi"
            html = f"""
            <html><body style="font-family:Arial,sans-serif;color:#333">
              <div style="max-width:600px;margin:0 auto;padding:20px">
                <h2 style="color:#2c3e50">Password Reset Request</h2>
                <p>Hi {first_name},</p>
                <p>Click below to reset your password.</p>
                <p><a href="{link}" style="display:inline-block;padding:10px 20px;background:#e74c3c;color:#fff;text-decoration:none;border-radius:5px">Reset Password</a></p>
                <p>Or copy this link: <code>{link}</code></p>
                <p style="color:#7f8c8d;font-size:12px">This link expires in 24 hours.</p>
                <hr><p style="color:#7f8c8d;font-size:12px">If you didn't request this, ignore this email.</p>
              </div>
            </body></html>"""
            return EmailSender._send_email(email, subject, html)
        except Exception as e:
            logger.error(f"Error sending password reset email: {e}")
            return False

    @staticmethod
    def _send_email(to_email: str, subject: str, html_body: str) -> bool:
        if not settings.smtp_user or not settings.smtp_password:
            logger.warning("SMTP credentials not configured; email not sent.")
            return False

        # Use smtp_user as sender if sender_email is a placeholder or not set
        from_email = settings.sender_email
        if not from_email or "bhoomi.local" in from_email:
            from_email = settings.smtp_user
            logger.info(f"Using SMTP user as sender: {from_email}")

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{settings.sender_name} <{from_email}>"
        msg["To"] = to_email
        msg.attach(MIMEText(html_body, "html"))

        # Attempt 1: STARTTLS on configured port (usually 587)
        try:
            logger.info(f"Attempt 1: STARTTLS to {settings.smtp_server}:{settings.smtp_port}")
            with smtplib.SMTP(settings.smtp_server, settings.smtp_port, timeout=15) as srv:
                srv.ehlo()
                srv.starttls()
                srv.ehlo()
                srv.login(settings.smtp_user, settings.smtp_password)
                srv.sendmail(from_email, to_email, msg.as_string())
            logger.info(f"Email sent to {to_email} via STARTTLS")
            return True
        except Exception as e1:
            logger.warning(f"STARTTLS failed: {type(e1).__name__}: {e1}")

        # Attempt 2: SMTP_SSL on port 465
        try:
            logger.info(f"Attempt 2: SMTP_SSL to {settings.smtp_server}:465")
            with smtplib.SMTP_SSL(settings.smtp_server, 465, timeout=15) as srv:
                srv.login(settings.smtp_user, settings.smtp_password)
                srv.sendmail(from_email, to_email, msg.as_string())
            logger.info(f"Email sent to {to_email} via SMTP_SSL")
            return True
        except Exception as e2:
            logger.error(f"SMTP_SSL also failed: {type(e2).__name__}: {e2}")

        logger.error(f"All email delivery attempts failed for {to_email}")
        return False
