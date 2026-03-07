# User Authentication System - Complete Guide

## Overview

Your Bhoomi platform now includes a complete user authentication system with:
- ✅ User registration (Citizen, Lawyer, Court Staff)
- ✅ User login with secure token-based sessions
- ✅ User dashboard for tracking and profile management
- ✅ Saved searches and activity tracking
- ✅ Responsive design for all devices

---

## 🚀 Quick Start

### Demo Account
**For testing purposes**, a demo account has been created:
- **Username:** `demo`
- **Password:** `demo123`

Use this to explore all features without creating a new account.

### Create Your Account

1. Go to **[http://localhost:8000/static/register.html](http://localhost:8000/static/register.html)**
2. Click "Register here" button from login page
3. Fill in your details:
   - Choose user type (Citizen, Lawyer, or Court Staff)
   - First name, last name, email
   - Create username and password
4. Click "Create Account"
5. You'll be redirected to login page

### Login to Your Account

1. Go to **[http://localhost:8000/static/login.html](http://localhost:8000/static/login.html)**
2. Enter username and password
3. **Optional:** Check "Remember me" to stay logged in
4. Click "Login"
5. You'll be redirected to your dashboard

---

## 📋 User Types

### 1. Citizen
- Access public case information
- Search by village and survey number
- Track specific land cases
- Save frequently searched cases
- View case details and documents

### 2. Lawyer / Advocate
- All citizen features, plus:
- Professional account designation
- Statistics dashboard (cases tracked, hearings, documents)
- Advanced filtering capabilities
- Professional profile

### 3. Court Staff
- All lawyer features, plus:
- Official court representative status
- Direct case management tools
- Enhanced statistics
- Court-specific access

---

## 🔐 Authentication Details

### Token-Based System
- Uses secure random tokens (32-byte).
- Tokens stored in `users.json` and `user_tokens.json`
- Sessions can be browser-based (sessionStorage) or persistent (localStorage)

### File Storage
```
backend/app/data/
├── users.json          # User account data (hashed passwords)
├── user_tokens.json    # Active session tokens
└── sample_parcels.json # Court case data
```

### Security
- Passwords hashed using SHA256
- Tokens are cryptographically secure
- CORS enabled for frontend access
- All auth endpoints require validation

---

## 📱 User Pages

### 1. Registration Page
**URL:** [http://localhost:8000/static/register.html](http://localhost:8000/static/register.html)

**Features:**
- Select user type (Citizen, Lawyer, Court Staff)
- Auto-populated field descriptions
- Real-time validation
- Password strength indicators
- Link to login page

**Fields:**
- First Name (required)
- Last Name (optional)
- Email (required)
- Username (4-20 chars, alphanumeric + underscore)
- Password (6+ chars, letters + numbers)
- Confirm Password

### 2. Login Page
**URL:** [http://localhost:8000/static/login.html](http://localhost:8000/static/login.html)

**Features:**
- Demo credentials displayed
- Password visibility toggle
- "Remember me" checkbox
- Error handling
- Links to registration and main search

**Demo Account:**
```
Username: demo
Password: demo123
```

### 3. User Dashboard
**URL:** [http://localhost:8000/static/dashboard.html](http://localhost:8000/static/dashboard.html)

**Sections:**
1. **Welcome** - Personalized greeting
2. **Quick Actions**
   - Search Cases
   - Edit Profile (coming soon)
   - Download Data
3. **Profile Card**
   - Email, Username, Account Type
   - Member Since, Last Login
4. **Statistics Card** (Lawyers & Court Staff only)
   - Cases Tracked
   - Hearings This Month
   - Documents Uploaded
5. **Recent Activity**
   - List of recent actions
6. **Saved Searches**
   - Quick access to saved case searches
   - Delete option

### 4. Main Search Page (Enhanced)
**URL:** [http://localhost:8000/](http://localhost:8000/)

**New Features:**
- User navigation header at top
- Login/Register buttons (for non-logged-in users)
- Dashboard & Logout buttons (for logged-in users)
- User name display
- Responsive design

---

## 🔌 API Endpoints

### User Registration
```
POST /api/v1/auth/register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123",
  "first_name": "John",
  "last_name": "Doe",
  "user_type": "citizen"  // "citizen" | "lawyer" | "court_staff"
}

Response (201 Created):
{
  "status": "ok",
  "message": "User registered successfully",
  "user": {
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "user_type": "citizen"
  }
}
```

### User Login
```
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "johndoe",
  "password": "SecurePass123"
}

Response (200 OK):
{
  "status": "ok",
  "token": "alc_Jo7JeL51mbjz4ro5...",
  "user": {
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "user_type": "citizen",
    "created_at": "2026-03-05T10:30:00"
  }
}
```

### Get User Profile
```
GET /api/v1/auth/profile
Authorization: Bearer <token>
OR
X-Admin-Token: <token>

Response (200 OK):
{
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "user_type": "citizen",
  "created_at": "2026-03-05T10:30:00",
  "updated_at": "2026-03-05T10:30:00"
}
```

### User Logout
```
POST /api/v1/auth/logout
Authorization: Bearer <token>

Response (200 OK):
{
  "status": "ok",
  "message": "Logged out successfully"
}
```

---

## 💾 Frontend Session Management

### Storing User Data
After successful login, user data is stored in browser:

**localStorage** (if "Remember me" checked):
```javascript
localStorage.setItem('user_token', token);
localStorage.setItem('user_data', JSON.stringify(user));
```

**sessionStorage** (default):
```javascript
sessionStorage.setItem('user_token', token);
sessionStorage.setItem('user_data', JSON.stringify(user));
```

### Accessing User Data in Frontend
```javascript
// Get token
const token = localStorage.getItem('user_token') || sessionStorage.getItem('user_token');

// Get user data
const userData = JSON.parse(
  localStorage.getItem('user_data') || 
  sessionStorage.getItem('user_data') || 
  '{}'
);

// Check if logged in
if (token && userData.username) {
  console.log('User:', userData.first_name);
}
```

### Logging Out
```javascript
localStorage.removeItem('user_token');
localStorage.removeItem('user_data');
sessionStorage.removeItem('user_token');
sessionStorage.removeItem('user_data');
window.location.href = '/static/login.html';
```

---

## 🎯 Using Saved Searches

### Save a Search
After searching for a case, you can save it for quick access:
```javascript
// Save search
const search = {
  label: "My Land Case",
  village: "Kisanpur",
  survey: "123"
};

let saved = JSON.parse(localStorage.getItem('saved_searches') || '[]');
saved.push(search);
localStorage.setItem('saved_searches', JSON.stringify(saved));
```

### Use Saved Search
Saved searches appear on dashboard:
1. Click "Use" button next to saved search
2. Automatically redirected to search page with those parameters
3. Results load instantly

### Delete Saved Search
Click "Delete" button next to any saved search to remove it.

---

## 📊 Activity Tracking

### Track User Activity
Activities are automatically logged:
```javascript
// Add activity
const activity = {
  action: "Searched for case C123/2024",
  timestamp: new Date().toISOString()
};

let activities = JSON.parse(localStorage.getItem('user_activity') || '[]');
activities.push(activity);
localStorage.setItem('user_activity', JSON.stringify(activities));
```

### View Activity
1. Go to Dashboard
2. Scroll to "Recent Activity" section
3. See last 5 activities

---

## 🔍 Testing the Authentication System

### Test Registration (cURL)
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

### Test Login (cURL)
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "Test123"
  }'
```

### Test Profile (cURL)
```bash
TOKEN="alc_Jo7JeL51mbjz4ro5..."
curl -X GET http://localhost:8000/api/v1/auth/profile \
  -H "Authorization: Bearer $TOKEN"
```

### Test with PowerShell
```powershell
# Register
$body = @{
    username = "psuser"
    email = "ps@example.com"
    password = "PsUser123"
    first_name = "PowerShell"
    user_type = "citizen"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/auth/register" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body

$response.Content | ConvertFrom-Json
```

---

## ⚙️ Configuration

### Environment Variables
```bash
# Can be set to override defaults

# Admin token for case management
ADMIN_TOKEN=devtoken123

# Debug mode
DEBUG=false

# Logging level
LOG_LEVEL=INFO
```

### Backend Files Modified
- `backend/app/main.py` - Added auth endpoints
- `backend/app/data/users.json` - User database
- `backend/app/data/user_tokens.json` - Session tokens

### Frontend Files Created
- `backend/app/static/register.html` - Registration form
- `backend/app/static/login.html` - Login form
- `backend/app/static/dashboard.html` - User dashboard

### Frontend Files Updated
- `backend/app/static/index.html` - Added user navigation

---

## 🛡️ Security Best Practices

### For Users
✅ **DO:**
- Use strong, unique passwords (letters + numbers + symbols)
- Enable "Remember me" only on personal devices
- Logout after using on shared computers
- Verify your email address
- Check profile regularly

❌ **DON'T:**
- Share your password or token
- Use same password across sites
- Store sensitive data in browser
- Use publicly accessible computers
- Forget to logout on shared devices

### For Developers
✅ **DO:**
- Hash passwords before storing
- Validate all input
- Use HTTPS in production
- Implement rate limiting
- Audit access logs

❌ **DON'T:**
- Store passwords in plain text
- Expose error details
- Use weak token generation
- Skip authentication checks
- Enable debug mode in production

---

## 🐛 Troubleshooting

### "Invalid username or password"
- Check spelling and capitalization
- Username is case-sensitive
- Try demo account (demo/demo123) to verify system works

### "Username or email already exists"
- Username or email taken by another user
- Choose different username or email
- Try username with numbers: user123, user456

### Token not valid
- Token may have expired (clear browser cache)
- Try logging in again to get new token
- Ensure you're using correct storage (localStorage vs sessionStorage)

### Dashboard not loading
- Check browser console for errors
- Ensure you're logged in
- Clear localStorage/sessionStorage and login again

### Saved searches not appearing
- Verify you're using same browser
- Check localStorage is enabled
- Try saving again from search page

---

## 📈 Future Enhancements

Planned features for future versions:
- [ ] Email verification
- [ ] Password reset via email
- [ ] Two-factor authentication
- [ ] OAuth integration (Google, GitHub)
- [ ] Profile picture upload
- [ ] Case sharing with other users
- [ ] Advanced search filters
- [ ] PDF export of case documents
- [ ] Real-time notifications
- [ ] Mobile app

---

## 📞 Support

For issues or questions:
1. Check this guide first
2. Review troubleshooting section
3. Check browser console for errors
4. Verify server is running: `http://localhost:8000/health`
5. Clear browser cache and try again

---

## Summary

Your Bhoomi platform now has:
✅ Complete user authentication system
✅ Three user types with role-based access
✅ Secure token-based sessions
✅ User dashboard with activity tracking
✅ Saved searches functionality
✅ Responsive design for all devices
✅ Demo account for testing

**Start exploring:**
- [Register](http://localhost:8000/static/register.html)
- [Login](http://localhost:8000/static/login.html)
- [Search Cases](http://localhost:8000/)

