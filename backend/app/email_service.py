"""Email utility module for sending verification and password reset emails."""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta, timezone
from typing import Optional
import secrets
import json
import pathlib

try:
    from .config import get_settings
except ImportError:
    from config import get_settings

settings = get_settings()
logger = logging.getLogger("email")

BASE_DIR = pathlib.Path(__file__).parent
EMAIL_TOKENS_FILE = BASE_DIR / "data" / "email_tokens.json"


class EmailToken:
    """Manage email verification and password reset tokens."""
    
    @staticmethod
    def generate_token(email: str, token_type: str = "verify") -> str:
        """Generate a secure token for email verification or password reset.
        
        Args:
            email: Email address for token
            token_type: Either 'verify' or 'reset'
        
        Returns:
            Secure token string
        """
        token = secrets.token_urlsafe(32)
        
        tokens = EmailToken._load_tokens()
        tokens.append({
            "token": token,
            "email": email,
            "type": token_type,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "expires_at": (datetime.now(timezone.utc) + timedelta(
                hours=settings.email_verification_expiry_hours if token_type == "verify" 
                else settings.password_reset_expiry_hours
            )).isoformat(),
            "used": False,
            "used_at": None
        })
        EmailToken._save_tokens(tokens)
        
        return token
    
    @staticmethod
    def verify_token(token: str, token_type: str = "verify") -> Optional[str]:
        """Verify a token and return email if valid.
        
        Args:
            token: Token to verify
            token_type: Either 'verify' or 'reset'
        
        Returns:
            Email if token is valid and not expired, None otherwise
        """
        tokens = EmailToken._load_tokens()
        
        for entry in tokens:
            if entry.get("token") == token and entry.get("type") == token_type:
                # Check if not already used
                if entry.get("used"):
                    return None
                
                # Check if not expired
                expires_at = datetime.fromisoformat(entry.get("expires_at", ""))
                if datetime.now(timezone.utc) > expires_at:
                    return None
                
                return entry.get("email")
        
        return None
    
    @staticmethod
    def mark_token_used(token: str) -> bool:
        """Mark a token as used."""
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
        """Load email tokens from file."""
        try:
            if EMAIL_TOKENS_FILE.exists():
                with open(EMAIL_TOKENS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
        except:
            pass
        return []
    
    @staticmethod
    def _save_tokens(tokens: list):
        """Save email tokens to file."""
        EMAIL_TOKENS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(EMAIL_TOKENS_FILE, "w", encoding="utf-8") as f:
            json.dump(tokens, f, ensure_ascii=False, indent=2)


class EmailSender:
    """Send emails via SMTP."""
    
    @staticmethod
    def send_verification_email(email: str, first_name: str, verification_token: str, base_url: str = "http://192.168.56.1:8000") -> bool:
        """Send email verification link.
        
        Args:
            email: Recipient email
            first_name: User's first name
            verification_token: Verification token to include in link
            base_url: Base URL for verification link
        
        Returns:
            True if email sent successfully, False otherwise
        """
        if not settings.enable_email:
            logger.warning(f"Email is disabled. Skipping verification email for {email}")
            return True
        
        try:
            verification_link = f"{base_url}/static/verify-email.html?token={verification_token}"
            
            subject = "Verify Your Bhoomi Account - Action Required"
            
            html_body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #2c3e50;">Welcome to Bhoomi, {first_name}!</h2>
                        
                        <p>Thank you for registering. Please verify your email address to activate your account.</p>
                        
                        <p><strong>Your account details:</strong></p>
                        <ul>
                            <li>Email: {email}</li>
                            <li>Status: Pending Email Verification</li>
                        </ul>
                        
                        <p><a href="{verification_link}" style="display: inline-block; padding: 10px 20px; background-color: #3498db; color: white; text-decoration: none; border-radius: 5px;">
                            Verify Email
                        </a></p>
                        
                        <p>Or copy and paste this link in your browser:</p>
                        <p style="word-break: break-all; background-color: #ecf0f1; padding: 10px; border-radius: 3px;">
                            {verification_link}
                        </p>
                        
                        <p style="color: #7f8c8d; font-size: 12px;">
                            <strong>Note:</strong> This link will expire in 24 hours.
                        </p>
                        
                        <hr style="border: none; border-top: 1px solid #ecf0f1; margin: 20px 0;">
                        
                        <p style="color: #7f8c8d; font-size: 12px;">
                            If you didn't create this account, please ignore this email.
                        </p>
                    </div>
                </body>
            </html>
            """
            
            return EmailSender._send_email(email, subject, html_body)
        
        except Exception as e:
            logger.error(f"Error sending verification email: {e}")
            return False
    
    @staticmethod
    def send_password_reset_email(email: str, first_name: str, reset_token: str, base_url: str = "http://192.168.56.1:8000") -> bool:
        """Send password reset link.
        
        Args:
            email: Recipient email
            first_name: User's first name
            reset_token: Password reset token
            base_url: Base URL for reset link
        
        Returns:
            True if email sent successfully, False otherwise
        """
        if not settings.enable_email:
            logger.warning(f"Email is disabled. Skipping password reset email for {email}")
            return True
        
        try:
            reset_link = f"{base_url}/static/reset-password.html?token={reset_token}"
            
            subject = "Password Reset Request - Bhoomi"
            
            html_body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #2c3e50;">Password Reset Request</h2>
                        
                        <p>Hi {first_name},</p>
                        
                        <p>We received a request to reset your password. Click the button below to create a new password.</p>
                        
                        <p><a href="{reset_link}" style="display: inline-block; padding: 10px 20px; background-color: #e74c3c; color: white; text-decoration: none; border-radius: 5px;">
                            Reset Password
                        </a></p>
                        
                        <p>Or copy and paste this link:</p>
                        <p style="word-break: break-all; background-color: #ecf0f1; padding: 10px; border-radius: 3px;">
                            {reset_link}
                        </p>
                        
                        <p style="color: #7f8c8d; font-size: 12px;">
                            <strong>Note:</strong> This link will expire in 24 hours.
                        </p>
                        
                        <hr style="border: none; border-top: 1px solid #ecf0f1; margin: 20px 0;">
                        
                        <p style="color: #7f8c8d; font-size: 12px;">
                            If you didn't request a password reset, please ignore this email or contact support.
                        </p>
                    </div>
                </body>
            </html>
            """
            
            return EmailSender._send_email(email, subject, html_body)
        
        except Exception as e:
            logger.error(f"Error sending password reset email: {e}")
            return False
    
    @staticmethod
    def _send_email(to_email: str, subject: str, html_body: str) -> bool:
        """Send email via SMTP.
        
        Args:
            to_email: Recipient email
            subject: Email subject
            html_body: HTML email body
        
        Returns:
            True if successful, False otherwise
        """
        if not settings.smtp_user or not settings.smtp_password:
            logger.warning("SMTP credentials not configured. Email sending disabled.")
            return False
        
        try:
            # Create email message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{settings.sender_name} <{settings.sender_email}>"
            msg["To"] = to_email
            
            # Attach HTML body
            html_part = MIMEText(html_body, "html")
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(settings.smtp_server, settings.smtp_port, timeout=10) as server:
                server.starttls()
                server.login(settings.smtp_user, settings.smtp_password)
                server.sendmail(settings.sender_email, to_email, msg.as_string())
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False
