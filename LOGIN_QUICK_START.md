# User Login System - Quick Reference

## 🎯 Quick Access

| Feature | URL | Notes |
|---------|-----|-------|
| **Main Search** | [http://localhost:8000/](http://localhost:8000/) | Public search (login optional) |
| **Register** | [http://localhost:8000/static/register.html](http://localhost:8000/static/register.html) | Create new account |
| **Login** | [http://localhost:8000/static/login.html](http://localhost:8000/static/login.html) | Sign in to account |
| **Dashboard** | [http://localhost:8000/static/dashboard.html](http://localhost:8000/static/dashboard.html) | User profile & activity (login required) |
| **Forgot Password** | [http://localhost:8000/static/forgot-password.html](http://localhost:8000/static/forgot-password.html) | Reset password via email |

---

## 👤 Demo Account

**Test the system instantly without registering:**

```
Username: demo
Password: demo123
```

---

## ✨ Features

### For Logged-In Users
✅ View user dashboard
✅ Track search history
✅ Save favorite searches
✅ View recent activity
✅ Download account data
✅ Personalized greeting
✅ View profile information

### For All Users
✅ Search court cases by village & survey number
✅ View case details and FIR information
✅ Access land file information
✅ View Documents and sources

---

## 🔄 Login Flow

```
1. Go to Login Page
   ↓
2. Enter Username & Password
   ↓
3. (Optional) Check "Remember Me"
   ↓
4. Click Login
   ↓
5. Redirected to Dashboard
   ↓
6. Explore & Search Cases
```

---

## 📝 Create New Account

### Step 1: Go to Registration
[http://localhost:8000/static/register.html](http://localhost:8000/static/register.html)

### Step 2: Select User Type
- **Citizen** - Basic access to search cases
- **Lawyer** - Professional account with advanced features
- **Court Staff** - Official court representative access

### Step 3: Fill in Details
```
First Name:     John
Last Name:      Doe
Email:          john.doe@example.com
Username:       johndoe          (4-20 chars)
Password:       SecurePass123    (6+ chars, letters + numbers)
```

### Step 4: Verify & Create
- Check "Remember Me" choice
- Click "Create Account"
- Auto-redirect to login

### Step 5: Email Verification ✉️ NEW
- Check your email inbox for verification message from Bhoomi
- Click the "Verify Email" link in the email
- Your email will be confirmed automatically
- Email link expires in 24 hours

### Step 6: Login
- Use your new username & password
- Access dashboard immediately

---

## 🔐 Password Requirements

✅ At least 6 characters
✅ Contains letters (a-z, A-Z)
✅ Contains numbers (0-9)
❌ Do NOT use just letters or numbers alone

**Examples of valid passwords:**
- `Pass123` ✅
- `Security2024` ✅
- `Case#789` ✅
- ❌ `password` (no numbers)
- ❌ `123456` (no letters)

---

## 🔑 Forgot Your Password?

### Step 1: Go to Password Reset
[http://localhost:8000/static/forgot-password.html](http://localhost:8000/static/forgot-password.html)

### Step 2: Enter Your Email
- Use the email you registered with
- Click "Send Reset Link"

### Step 3: Check Email
- Look in your inbox for reset email
- Check spam folder if you don't see it
- Link expires in 24 hours

### Step 4: Reset Password
- Click link from email
- Enter new password (must have letters and numbers)
- Confirm new password matches
- Click "Reset Password"

### Step 5: Login Again
- Use your new password to login
- Go to [Login Page](http://localhost:8000/static/login.html)

- `MyPassword42` ✅
- `SecureCode999` ✅

**Examples of invalid passwords:**
- `password` ❌ (no numbers)
- `123456` ❌ (no letters)
- `Pass1` ❌ (too short)

---

## 🎛️ Navigation

### When NOT Logged In
Top navigation shows:
- [Bhoomi Logo/Home]
- [Login Button]
- [Register Button]

### When Logged In
Top navigation shows:
- [Bhoomi Logo/Home]
- [👤 Your Name]
- [Dashboard Button]
- [Logout Button]

---

## 📊 Dashboard Overview

### Profile Section
Shows your account information:
- Email
- Username
- Account Type (Citizen/Lawyer/Court Staff)
- Member Since
- Last Login

### Statistics (Lawyers & Court Staff only)
- Cases Tracked count
- Hearings This Month
- Documents Uploaded

### Recent Activity
- List of actions (searches, views)
- Timestamps for each action
- Up to 5 recent items

### Saved Searches
- Quick access to saved searches
- One-click to search again
- Delete option
- Shows village & survey number

### Quick Actions
- [Search Cases] - Go back to search
- [Edit Profile] - Coming soon
- [Download Data] - Export account data

---

## 💾 Remember Me Feature

### Enabled (Checked)
- Stores login info in browser
- Stays logged in after closing browser
- Good for personal computers

### Disabled (Unchecked)
- Uses temporary session storage
- Auto-logout when closing browser
- Better for shared computers

---

## 🚪 Logout

**Option 1: From Navigation**
- Click [Logout] button in top right
- Redirects to search page

**Option 2: From Dashboard**
- Click [Logout] button
- Confirms logout
- Clears stored data

---

## 🔍 Search After Login

### Public Search (No Login Required)
1. Go to [http://localhost:8000/](http://localhost:8000/)
2. Enter village name
3. Enter survey number
4. Click [Search]
5. View results

### Save Search (Login Required)
1. Perform a search
2. Results display
3. Results auto-saved to your activity
4. View on [Dashboard](http://localhost:8000/static/dashboard.html)

### Use Saved Search
1. Go to Dashboard
2. Find in "Saved Searches" section
3. Click [Use] button
4. Auto-filled search parameters
5. Results load instantly

---

## 📱 Mobile-Friendly

All pages are fully responsive:
- ✅ Mobile phones (320px+)
- ✅ Tablets (768px+)
- ✅ Desktops (1024px+)

---

## 🔗 User Types Comparison

| Feature | Citizen | Lawyer | Court Staff |
|---------|---------|--------|-------------|
| Search Cases | ✅ | ✅ | ✅ |
| View Details | ✅ | ✅ | ✅ |
| Save Searches | ✅ | ✅ | ✅ |
| Dashboard | ✅ | ✅ | ✅ |
| Statistics | ❌ | ✅ | ✅ |
| Professional Badge | ❌ | ✅ | ✅ |
| Advanced Filters | ❌ | ✅ | ✅ |

---

## ⚡ Quick Tips

💡 **Tip 1:** Use demo account to explore
- Username: `demo`
- Password: `demo123`

💡 **Tip 2:** "Remember Me" saves your login
- Check it on personal computers
- Leave unchecked on shared ones

💡 **Tip 3:** Dashboard shows all your activity
- Recent searches
- Saved cases
- Account information

💡 **Tip 4:** Download your data anytime
- Click "Download Data" button
- Exports as JSON file
- Personal backup of your info

💡 **Tip 5:** Logout on shared computers
- Always click Logout when done
- Clears all stored data
- Next user can't see your info

---

## 🆘 Common Issues

### "Email not verified"
→ Check your inbox for verification email
→ Click the verification link
→ Link expires in 24 hours
→ [Resend verification email](http://localhost:8000/static/resend-verification.html)

### "Invalid username or password"
→ Check caps lock
→ Verify spelling
→ Try demo: demo/demo123

### Forgot password?
→ Go to [Forgot Password](http://localhost:8000/static/forgot-password.html)
→ Enter your email
→ Click link in verification email
→ Create new password

### Didn't receive verification email?
→ Check spam/junk folder
→ Wait a few minutes (might be delayed)
→ [Resend verification email](http://localhost:8000/static/resend-verification.html)

### Can't see Dashboard?
→ Make sure you're logged in
→ Check if browser allows localStorage

### Saved Searches not showing?
→ Must be logged in
→ Search in same browser session
→ Clear cache and login again

---

## 🎯 Next Steps

1. **Try Demo:** Use demo/demo123 to explore
2. **Create Account:** [Register here](http://localhost:8000/static/register.html)
3. **Login:** [Sign in here](http://localhost:8000/static/login.html)
4. **Search:** Use [main page](http://localhost:8000/) to find cases
5. **Dashboard:** Visit [dashboard](http://localhost:8000/static/dashboard.html) when logged in

---

## 📚 Full Documentation

For complete details, see: **[USER_AUTHENTICATION_GUIDE.md](USER_AUTHENTICATION_GUIDE.md)**

Covers:
- Detailed API endpoints
- Backend implementation
- Security practices
- Troubleshooting
- Future enhancements

