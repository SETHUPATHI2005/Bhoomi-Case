# Complete Authentication Guide

## Important: Email Verification is Required

The Bhoomi platform requires email verification for security. Here's the complete authentication flow:

---

## Step 1: User Registration

1. Visit: `http://localhost:8000` → Click "Register" button
2. Fill in the registration form:
   - First Name
   - Last Name
   - Email Address (must be valid)
   - Username (4-20 characters)
   - Password (min 6 chars, letters + numbers)
   - Confirm Password

3. Click "Create Account"

**What happens:**
- Account is created
- Verification email is sent to your email address
- You see: "Registration successful! Verification email sent."

---

## Step 2: Email Verification (CRITICAL)

**You MUST verify your email before you can login!**

1. Check your email inbox (and spam/junk folder)
2. Look for email from: **Bhoomi Land Cases**
3. Click the "Verify Email" button in the email OR copy the verification link
4. You'll see: "✅ Email Verified Successfully! You can now login."

---

## Step 3: Login

1. Visit: `http://localhost:8000` → Click "Login" tab
2. Enter:
   - Username: (your username from registration)
   - Password: (your password from registration)
3. Click "Login"

**If you see error:** "Email not verified"
- Go back to Step 2 and verify your email
- Then try login again

**After successful login:**
- You'll be redirected to the Dashboard
- You can now search cases and add new cases

---

## Account Requirements

### Password Rules:
- ✓ Minimum 6 characters
- ✓ Must contain letters (A-Z, a-z)
- ✓ Must contain numbers (0-9)

Example good passwords:
- `password123`
- `Secure2024`
- `Bhoomi001`

### Username Rules:
- ✓ 4-20 characters
- ✓ Unique (no duplicates)
- ✓ Can contain letters, numbers, underscores

### Email:
- ✓ Must be valid (required for verification email)
- ✓ Must be unique (one account per email)

---

## Troubleshooting

### "Username already exists"
**Solution:** Choose a different username

### "Email already registered"
**Solution:** Use a different email address

### "Email not verified"
**Solution:** 
1. Check your email for verification link
2. Click the verification link
3. Try login again

### "Invalid password"
**Solution:** Check your password and try again

### Didn't receive verification email?
**Solution:**
1. Check spam/junk folder
2. Check if email was entered correctly during registration
3. Use "Resend Verification Email" link (if available)
4. Contact administrator if problem persists

---

## Testing with Demo Account

**Note:** Demo account is pre-verified and ready to use.

1. Username: `demo`
2. Password: `demo123`
3. Click "Login" and go directly to Dashboard

---

## Admin Access

If you are an administrator:

1. Go to Login page
2. Click "Admin Login" button
3. Enter Admin Credentials:
   - Admin Username
   - Admin Password
   - Admin Token (security code - provided separately)

4. You'll be redirected to Admin Panel where you can:
   - Manage cases
   - Edit/delete records
   - Manage users
   - View audit logs
   - System administration

---

## Complete User Journey

```
1. LANDING PAGE
   ↓ Click "Register"
   
2. REGISTER FORM
   ↓ Fill details & submit
   
3. EMAIL VERIFICATION
   ↓ Receive email → Click verification link
   
4. LOGIN PAGE
   ↓ Enter credentials → Click Login
   
5. DASHBOARD
   ✓ Access all user features
```

---

## FAQ

**Q: When will I receive the verification email?**
A: Usually within 1-2 minutes. Check spam folder if not in inbox.

**Q: Can I login without email verification?**
A: No, email verification is required for security.

**Q: How long is the verification link valid?**
A: 24 hours from registration.

**Q: What if I lose access to my registered email?**
A: Contact the administrator for account recovery.

**Q: Can I register multiple accounts?**
A: Each email address can only have one account.

**Q: How do I reset my password?**
A: Click "Forgot Password?" on the login page.

---

## API Endpoints (For Developers)

### Register User
```
POST /api/v1/auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123",
  "first_name": "John",
  "last_name": "Doe"
}

Response (201):
{
  "status": "ok",
  "message": "User registered successfully. Check your email to verify.",
  "user": { ... }
}
```

### Login User
```
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "SecurePass123"
}

Response (200):
{
  "status": "ok",
  "token": "eyJ0eXAiOiJKV1QiLCJh...",
  "user": { ... }
}
```

### Verify Email
```
POST /api/v1/auth/verify-email
Content-Type: application/json

{
  "token": "cSf1htWvjZYFw..." // from email link
}

Response (200):
{
  "status": "ok",
  "message": "Email verified successfully. You can now login."
}
```

### Request Password Reset
```
POST /api/v1/auth/request-password-reset
Content-Type: application/json

{
  "email": "john@example.com"
}

Response (200):
{
  "status": "ok",
  "message": "Password reset link sent to email"
}
```

### Reset Password
```
POST /api/v1/auth/reset-password
Content-Type: application/json

{
  "token": "xyzabc...", // from email link
  "new_password": "NewPass456"
}

Response (200):
{
  "status": "ok",
  "message": "Password reset successfully"
}
```

---

**Version:** 1.0.0  
**Last Updated:** March 5, 2026  
**Status:** Production Ready
