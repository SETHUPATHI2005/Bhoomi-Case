# Bhoomi Application User Journey

## Application Flow Architecture

### 1. Landing Page (Entry Point)
**URL:** `http://localhost:8000/` or `http://192.168.56.1:8000/`

**Page:** `landing.html`

**Features:**
- ✓ Service description and features
- ✓ About Bhoomi and its mission
- ✓ Development team information
- ✓ Key features overview
- ✓ Call-to-action buttons: Login / Register

**Purpose:** First impression, introduction to the platform

---

## 2. Authentication Flow

### User Landing Page
**URL:** `http://localhost:8000/static/auth.html`

**Page:** `auth.html` (Unified Login/Register Interface)

**Two Tabs:**

#### A. Login Tab
**For Existing Users**
- Username
- Password
- "Forgot Password?" link
- "Admin Login" button (separate secure interface)

**Flow:**
1. User enters credentials
2. System validates against stored users
3. On success: Generate JWT token
4. Redirect to Dashboard
5. On failure: Display error message

#### B. Register Tab
**For New Users**
- First Name
- Last Name
- Email Address
- Username
- Password
- Confirm Password

**Flow:**
1. User fills registration form
2. System validates data
3. Creates user account
4. Sends verification email
5. Redirects to email verification page
6. User verifies email via link
7. Account activated, can now login

---

## 3. User Dashboard (After Login)
**URL:** `http://localhost:8000/static/dashboard.html`

**Page:** `dashboard.html`

**Features:**
- ✓ Search cases by village, survey number, case ID
- ✓ View search results with case details
- ✓ **Add New Case** functionality (coming soon)
- ✓ User profile information
- ✓ Logout button

**Purpose:** Main workspace for regular users to:
- Search existing cases
- Add new cases
- View case details
- Access their submitted cases

**Access Control:** Requires valid JWT token from login

---

## 4. Case Detail View
**URL:** `http://localhost:8000/static/case.html?id=<case_id>`

**Page:** `case.html`

**Features:**
- ✓ View complete case information
- ✓ Document links
- ✓ Case history
- ✓ Related cases
- ✓ Back to dashboard link

**Purpose:** Detailed view of individual cases

---

## 5. Admin Panel (Separate Secure Access)
**URL:** `http://localhost:8000/static/admin-login.html`

**Page:** `admin-login.html`

**Admin Login Process:**
1. Navigate to admin console
2. Enter Admin Username
3. Enter Admin Password
4. Enter Admin Token (security code)

**Security Features:**
- Separate login interface with warning banner
- Restricted access area notification
- Admin token requirement (additional security)
- All login attempts logged

### Admin Dashboard
**URL:** `http://localhost:8000/static/admin.html`

**Features:**
- ✓ Manage cases (Create, Read, Update, Delete)
- ✓ Edit case details
- ✓ Delete case records
- ✓ Upload new parcels/cases
- ✓ Bulk ingest data
- ✓ View audit logs
- ✓ User management (view/edit/delete)
- ✓ System administration tools

**Admin Responsibilities:**
- Manage case records and documents
- Control user access and permissions
- Monitor audit logs and activities
- System configuration and maintenance

**Access Control:**
- Requires admin username/password
- Requires separate admin token
- Only accessible to authorized administrators
- All actions logged for audit trail

---

## Complete User Journey Flow Chart

```
┌─────────────────────────────────────┐
│   Landing Page (landing.html)       │
│   - Service Info / Features         │
│   - About / Team                    │
│   - Login / Register buttons        │
└────────────┬────────────────────────┘
             │
      ┌──────┴──────┐
      │             │
      ▼             ▼
┌──────────────┐  ┌──────────────┐
│ New User?    │  │ Existing     │
│ Register     │  │ User? Login  │
│              │  │              │
│ (auth.html)  │  │ (auth.html)  │
├──────────────┤  └──────────────┘
│ - Fill Form  │         │
│ - Verify     │         │
│   Email      │         ▼
│ - Create     │  ┌──────────────┐
│   Account    │  │ Check Creds  │
│              │  │ Generate JWT │
│              │  │              │
└──────────────┘  └──────────────┘
      │                  │
      └──────────┬───────┘
                 │
                 ▼
        ┌──────────────────┐
        │ User Dashboard   │
        │ (dashboard.html) │
        ├──────────────────┤
        │ - Search Cases   │
        │ - View Results   │
        │ - Add Case       │
        │ - Logout Button  │
        └────────┬─────────┘
                 │
      ┌──────────┴──────────┐
      │                     │
      ▼                     ▼
   ┌────────────┐   ┌──────────────┐
   │ View Case  │   │ Add New Case │
   │ Details    │   │ (Coming Soon)│
   │(case.html) │   └──────────────┘
   └────────────┘
```

---

## Admin Access Separate Path

```
┌──────────────────────────────────────┐
│   User Login Page (auth.html)        │
│   + Admin Login Button               │
└────────────┬─────────────────────────┘
             │
             ▼
   ┌──────────────────────────┐
   │ Admin Console Login      │
   │ (admin-login.html)       │
   ├──────────────────────────┤
   │ ⚠️ Restricted Access     │
   │ - Admin Username         │
   │ - Admin Password         │
   │ - Admin Token (Security) │
   │ + Audit Logging          │
   └────────────┬─────────────┘
                │
                ▼
   ┌──────────────────────────┐
   │ Admin Dashboard          │
   │ (admin.html)             │
   ├──────────────────────────┤
   │ ✓ Manage Cases           │
   │ ✓ Edit/Delete Records    │
   │ ✓ Upload Data            │
   │ ✓ Audit Logs             │
   │ ✓ User Management        │
   │ ✓ System Config          │
   └──────────────────────────┘
```

---

## Authentication & Security Features

### For Regular Users:
- Email verification required
- Password reset via email
- JWT token-based authentication
- Token expiration (24 hours)
- Session management

### For Administrators:
- Separate login interface
- Username + Password + Token (3-factor)
- Audit logging of all admin actions
- IP address tracking
- Admin token requirement (additional security layer)
- Restricted access warning

---

## Page Mapping Summary

| Page | File | URL | Purpose | Access |
|------|------|-----|---------|--------|
| Landing | landing.html | / | Introduction & navigation | Public |
| Auth (Login/Register) | auth.html | /static/auth.html | User authentication | Public |
| Dashboard | dashboard.html | /static/dashboard.html | User workspace | Authenticated users |
| Case Detail | case.html | /static/case.html | View case info | Authenticated users |
| Admin Login | admin-login.html | /static/admin-login.html | Admin authentication | Authorized admin users |
| Admin Panel | admin.html | /static/admin.html | Admin workspace | Authenticated admins |
| Email Verify | verify-email.html | /static/verify-email.html | Email confirmation | Users with token |
| Password Reset | reset-password.html | /static/reset-password.html | Password recovery | Users with token |
| Forgot Password | forgot-password.html | /static/forgot-password.html | Request password reset | Public |

---

## User Experience Timeline

### First-Time User:
1. Lands on landing.html (public welcome page)
2. Clicks "Register" → goes to auth.html
3. Fills registration form
4. Receives verification email
5. Clicks verification link
6. Email confirmed → can login
7. Logs in with credentials
8. Redirected to dashboard.html
9. Can search cases and add new cases

### Returning User:
1. Lands on landing.html
2. Clicks "Login" → goes to auth.html
3. Enters credentials
4. Automatically redirected to dashboard.html
5. Can access all user features

### Administrator:
1. Lands on landing.html
2. Clicks "Login" → goes to auth.html
3. Clicks "Admin Login" → goes to admin-login.html
4. Enters admin credentials + token
5. Redirected to admin.html
6. Can manage cases, users, and system

---

## Getting Started

### Start the Application:
```bash
cd "C:\Users\wwwse\OneDrive\Desktop\Bhoomi Case\backend\app"
python -m uvicorn main:app --reload
```

### Visit the Landing Page:
```
http://localhost:8000
or
http://192.168.56.1:8000
```

### User Registration:
1. Click "Register" on landing page
2. Complete registration form
3. Verify email address
4. Login with credentials

### Admin Access:
1. Go to Login page
2. Click "Admin Login" button
3. Enter admin credentials + token
4. Access admin panel

---

**Version:** 1.0.0  
**Date:** March 5, 2026  
**Platform:** Digital Justice Platform - Bhoomi
