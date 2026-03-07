# Admin Account Setup - Quick Start Guide

Welcome! This guide shows you how to use your admin account to manage Land Cases Search.

## 🔑 Your Admin Token

```
Token: devtoken123
```

This is your **admin credential**. Keep it safe!

## 📍 Access Points

### Admin Panel (Web UI)
```
http://localhost:8000/static/admin.html
```

### Public Search
```
http://localhost:8000/
```

## 🚀 How to Use Admin Features

### 1. Upload a Single Parcel

**Method**: POST  
**Endpoint**: `http://localhost:8000/api/v1/admin/upload`

**Using Admin Panel (Recommended)**:
1. Visit: http://localhost:8000/static/admin.html
2. Go to "Upload Parcel" tab
3. Paste token: `devtoken123`
4. Fill in the form:
   - Village: `Kisanpur`
   - Survey Number: `124`
   - Coordinates (optional): `28.7041,77.1025`
   - Linked Cases (optional): `["C124/2025"]`
5. Click "Upload Parcel"

**Using cURL**:
```bash
curl -X POST http://localhost:8000/api/v1/admin/upload \
  -H "Authorization: Bearer devtoken123" \
  -H "Content-Type: application/json" \
  -d '{
    "village": "Kisanpur",
    "survey_number": "124",
    "coordinates": "28.7041,77.1025",
    "linked_cases": ["C124/2025"]
  }'
```

### 2. Verify Your Upload

After uploading, verify it exists:

```bash
curl "http://localhost:8000/api/v1/search?village=Kisanpur&survey=124"
```

Expected response:
```json
{
  "count": 1,
  "results": [
    {
      "village": "Kisanpur",
      "survey_number": "124",
      "linked_cases": ["C124/2025"],
      "created_at": "2026-03-04T..."
    }
  ]
}
```

### 3. View Uploaded Data

**Admin Panel**:
1. Visit: http://localhost:8000/
2. Enter "Kisanpur" in Village field
3. Enter "124" in Survey field
4. Click "Search"
5. You should see your uploaded parcel

## 🔐 Authentication Methods

Your admin token can be sent in two ways:

**Method 1: Authorization Header (Recommended)**
```
Authorization: Bearer devtoken123
```

**Method 2: X-Admin-Token Header**
```
X-Admin-Token: devtoken123
```

## 📊 Sample Data to Upload

### Example 1: Single Property Record
```json
{
  "village": "Kisanpur",
  "survey_number": "125",
  "coordinates": "28.7041,77.1025",
  "linked_cases": ["C125/2024"]
}
```

### Example 2: With Court Case Details
```json
{
  "village": "Kisanpur",
  "survey_number": "126",
  "coordinates": "28.7041,77.1025",
  "linked_cases": [
    {
      "case_id": "C126/2024",
      "court": "District Court, Bhoomi",
      "parties": ["Property Owner A", "Property Owner B"],
      "status": "ongoing",
      "filed_date": "2024-03-01",
      "last_hearing_date": "2025-12-15",
      "documents": [
        {
          "title": "FIR",
          "url": "https://example.com/documents/c126_fir.pdf"
        }
      ],
      "source": {
        "name": "District Court Portal",
        "url": "https://court.example.com/cases/C126/2024",
        "retrieved_at": "2026-03-04T10:00:00Z"
      }
    }
  ]
}
```

## ✅ Common Tasks

### Change Admin Token
Edit `.env` file:
```
ADMIN_TOKEN=your_new_token_here
```

Then restart the server:
```bash
# Kill current server (Ctrl+C)
# Restart it
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

### Test Admin Access
```bash
curl -I -H "Authorization: Bearer devtoken123" \
  http://localhost:8000/api/v1/admin/upload
```

If you see `405 Method Not Allowed`, authentication is working ✓

### View All Data Uploaded
```bash
curl "http://localhost:8000/api/v1/search?village=&survey=" 2>/dev/null | head -20
```

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Missing admin token" | Make sure you're sending the Authorization header |
| "Invalid admin token" | Check that token is `devtoken123` exactly |
| Upload shows "400 Bad Request" | Verify village & survey_number fields are not empty |
| Search returns no results | Make sure you're using exact village & survey names |
| Server says "not found" | Visit http://localhost:8000/health to verify server is running |

## 📋 API Endpoints

| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/health` | GET | No | Check server status |
| `/api/v1/search` | GET | No | Search for cases (public) |
| `/api/v1/cases/{id}` | GET | No | Get case details (public) |
| `/api/v1/admin/upload` | POST | **Yes** | Upload parcel data (**ADMIN ONLY**) |
| `/` | GET | No | Access web UI |
| `/static/admin.html` | GET | No | Access admin panel |

## 🎯 Next Steps

1. **Upload Sample Data**: Use the admin panel to upload a test parcel
2. **Verify Search**: Search for your uploaded data using the public UI
3. **Change Token**: Update `ADMIN_TOKEN` in `.env` for security
4. **Load Production Data**: Prepare CSV/JSON files with actual court records

---

**Your Admin Account is Ready!**  
Admin Token: `devtoken123`  
Server: http://localhost:8000/

Need help? Check [PRODUCTION_README.md](../PRODUCTION_README.md) for more details.
