# Email Verification & Password Reset System

## Overview

The Bhoomi platform now includes a complete email verification and password reset system to ensure secure user registration and account recovery. This guide covers all aspects of the system for users, administrators, and developers.

---

## 🚀 Quick Start for Users

### Registration Process

1. **Create Account**
   - Go to [http://localhost:8000/static/register.html](http://localhost:8000/static/register.html)
   - Fill in your details (first name, email, username, password, etc.)
   - Select your user type (Citizen, Lawyer, Court Staff)
   - Click "Create Account"

2. **Verify Email**
   - Check your email inbox for a verification message from Bhoomi
   - Click the verification link in the email
   - Your email will be confirmed, and you can now login

3. **Login**
   - Go to [http://localhost:8000/static/login.html](http://localhost:8000/static/login.html)
   - Enter your username and password
   - Click "Login"

### Password Recovery

1. **Forgot Your Password?**
   - Go to [http://localhost:8000/static/login.html](http://localhost:8000/static/login.html)
   - Click "Forgot password?" link
   - Enter your email address
   - Click "Send Reset Link"

2. **Reset Your Password**
   - Check your email for password reset link
   - Click the link to open the reset form
   - Enter your new password (must contain letters and numbers)
   - Click "Reset Password"
   - Now you can login with your new password

### Resend Verification Email

If you didn't receive your verification email:

1. Go to [http://localhost:8000/static/login.html](http://localhost:8000/static/login.html)
2. Click on "Need to resend verification?" (or go to [http://localhost:8000/static/resend-verification.html](http://localhost:8000/static/resend-verification.html))
3. Enter your email address
4. Click "Resend Email"

---

## 🔐 Security Features

### Email Verification
- **Purpose**: Ensures users own the email address they registered with
- **Token Expiration**: 24 hours
- **One-Time Use**: Tokens can only be used once
- **Secure Tokens**: Uses cryptographically secure random tokens

### Password Reset
- **Purpose**: Allows users to recover accounts when they forget passwords
- **Token Expiration**: 24 hours
- **One-Time Use**: Reset tokens expire after use
- **Requirements**: New password must contain:
  - At least 6 characters
  - At least one letter (a-z, A-Z)
  - At least one number (0-9)

### Email Security
- Passwords hashed using SHA256
- Tokens stored securely
- No sensitive data in emails
- Rate limiting on email sends (planned)

---

## 📧 Email Pages

### 1. Registration Page
**URL**: [http://localhost:8000/static/register.html](http://localhost:8000/static/register.html)

**Process**:
1. Fill in required information
2. Click "Create Account"
3. Receive confirmation with instructions
4. Check email for verification link

### 2. Forgot Password Page
**URL**: [http://localhost:8000/static/forgot-password.html](http://localhost:8000/static/forgot-password.html)

**Process**:
1. Enter email address
2. Receive reset link via email
3. Click link to reset password
4. Receive confirmation

### 3. Email Verification Page
**URL**: [http://localhost:8000/static/verify-email.html?token=...](http://localhost:8000/static/verify-email.html)

**Features**:
- Automatically verifies email using token from link
- Shows success/error status
- Redirects to login after verification

### 4. Password Reset Page
**URL**: [http://localhost:8000/static/reset-password.html?token=...](http://localhost:8000/static/reset-password.html)

**Features**:
- Security requirements display
- Real-time validation
- Password strength feedback
- Clear error messages

---

## 🔧 API Endpoints

### Registration & Verification

#### POST /api/v1/auth/register
Register a new user and send verification email.

**Request**:
```json
{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123",
    "first_name": "John",
    "last_name": "Doe",
    "user_type": "citizen"
}
```

**Response** (201):
```json
{
    "status": "ok",
    "message": "User registered successfully. Please check your email to verify your account.",
    "user": {
        "username": "johndoe",
        "email": "john@example.com",
        "first_name": "John",
        "user_type": "citizen"
    }
}
```

#### POST /api/v1/auth/verify-email
Verify email address using token.

**Request**:
```json
{
    "token": "secure_token_from_email"
}
```

**Response** (200):
```json
{
    "status": "ok",
    "message": "Email verified successfully. You can now login."
}
```

#### POST /api/v1/auth/resend-verification-email
Resend verification email to user.

**Request**:
```json
{
    "email": "john@example.com"
}
```

**Response** (200):
```json
{
    "status": "ok",
    "message": "Verification email sent successfully"
}
```

### Password Reset

#### POST /api/v1/auth/request-password-reset
Request password reset link.

**Request**:
```json
{
    "email": "john@example.com"
}
```

**Response** (200):
```json
{
    "status": "ok",
    "message": "If email exists, password reset link has been sent"
}
```

#### POST /api/v1/auth/reset-password
Reset password using token.

**Request**:
```json
{
    "token": "reset_token_from_email",
    "password": "NewSecurePass123"
}
```

**Response** (200):
```json
{
    "status": "ok",
    "message": "Password reset successfully. You can now login with your new password."
}
```

---

## ⚙️ Configuration

### Email Configuration

Set these environment variables to enable email sending:

```bash
# SMTP Server
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SENDER_EMAIL=noreply@bhoomi.local
SENDER_NAME=Bhoomi Land Cases

# Optional Settings
ENABLE_EMAIL=true
EMAIL_VERIFICATION_EXPIRY_HOURS=24
PASSWORD_RESET_EXPIRY_HOURS=24
```

### For Gmail Users

1. Enable 2-Factor Authentication
2. Generate an App Password (not your regular password)
3. Use the App Password in `SMTP_PASSWORD`

### For Other Email Providers

Check your email provider's SMTP settings:
- **Outlook**: smtp.outlook.com:587
- **SendGrid**: smtp.sendgrid.net:587
- **AWS SES**: email-smtp.region.amazonaws.com:587

---

## 📂 File Storage

Email verification data is stored in:

```
backend/app/data/
├── users.json              # User accounts with verification status
├── user_tokens.json        # Active session tokens
├── email_tokens.json       # Email verification & reset tokens
└── admin_uploads.json      # Admin uploaded parcels
```

### Token Structure (email_tokens.json)

```json
[
    {
        "token": "secure_token_string",
        "email": "user@example.com",
        "type": "verify",
        "created_at": "2024-03-05T10:30:00+00:00",
        "expires_at": "2024-03-06T10:30:00+00:00",
        "used": false,
        "used_at": null
    }
]
```

---

## 👤 Demo Account

**For Testing Without Email**:

```
Username: demo
Password: demo123

Note: Demo account is pre-verified and ready to use.
```

---

## 🐛 Troubleshooting

### Not receiving verification emails?

1. **Check spam folder** - emails might be filtered
2. **Verify SMTP settings** - ensure credentials are correct
3. **Check email logs** - review server logs for errors:
   ```bash
   tail -f logs/application.log
   ```
4. **Resend email** - use the resend verification endpoint

### Can't reset password?

1. **Email address**: Ensure you entered the correct email
2. **Token expiration**: Reset links expire after 24 hours
3. **Password requirements**: Password must have letters and numbers
4. **Browser cache**: Clear cache and try again

### Token errors?

| Error | Cause | Solution |
|-------|-------|----------|
| "Invalid or expired token" | Token expired or already used | Request new email |
| "Token not found" | Wrong token or typo | Check email link carefully |
| "Email already verified" | Already verified | Proceed to login |

---

## 🔄 Development Notes

### Adding Custom Email Templates

Email templates are defined in `backend/app/email.py`:

1. **Verification Email**: `EmailSender.send_verification_email()`
2. **Reset Email**: `EmailSender.send_password_reset_email()`

To customize:
1. Edit the HTML templates in the respective functions
2. Modify colors, text, links, and branding
3. Restart the server for changes to take effect

### Testing Email Functionality

#### Test verification flow:
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "Test123",
    "first_name": "Test",
    "user_type": "citizen"
  }'
```

#### Test password reset:
```bash
curl -X POST http://localhost:8000/api/v1/auth/request-password-reset \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'
```

---

## ✅ Future Enhancements

- [ ] Two-factor authentication (2FA)
- [ ] Social login (Google, Microsoft)
- [ ] Email address change functionality
- [ ] Account recovery codes
- [ ] Login attempt notifications
- [ ] Session management improvements
- [ ] Passwordless authentication

---

## 📞 Support

For issues or questions about email verification:

1. Check the logs: `backend/app/logs/`
2. Review SMTP configuration
3. Test with demo account
4. Check email provider settings

---

**Last Updated**: March 5, 2026
**Version**: 1.0.0
