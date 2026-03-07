# Admin Upload Guide - Complete Fields Reference

## 🔐 Admin Credentials
- **Token**: `devtoken123`
- **Access URL**: http://localhost:8000/static/admin.html

---

## 📋 Complete Parcel & Case Data Structure

### **Required Fields** (Minimum to upload)
```json
{
  "village": "Village Name",
  "survey_number": "123"
}
```

### **Complete Fields** (All available options)

#### 1. **Parcel Information**
```json
{
  "village": "Kisanpur",
  "survey_number": "123",
  "property_type": "Agricultural Land|Residential|Commercial|Industrial|Mixed Agricultural",
  "area_sqft": 4500,
  "area_acres": 0.103,
  "coordinates": "28.7041,77.1025"
}
```

#### 2. **Location Details** ✨ NEW
```json
{
  "location": {
    "latitude": 28.7041,
    "longitude": 77.1025,
    "exact_location": "Near Kisanpur Primary School, Main Road",
    "district": "Bhoomi",
    "state": "Telangana",
    "pin_code": "500001"
  }
}
```

#### 3. **Land File Records** 📄 NEW
```json
{
  "land_file": {
    "mutation_number": "MUT-2020-1234",
    "original_owner": "Hari Ram Singh",
    "owner_since": "1995",
    "transfer_history": [
      {
        "from": "Hari Ram Singh",
        "to": "Ram Kumar Singh",
        "date": "2015-06-20",
        "deed_number": "DEED-2015-5678"
      }
    ],
    "rtc_number": "RTC-2024-9876",
    "pattadar_passbook": "PPB-123-2024",
    "land_registration_certificate": "LRC-123/2015"
  }
}
```

#### 4. **Court Cases** 📜
```json
{
  "linked_cases": [
    {
      "case_id": "C123/2024",
      "case_number": "OS.NO.234/2024",
      "court": "District Court - Bhoomi",
      "bench": "Civil Division - I",
      "case_type": "Original Suit - Land Dispute",
      "parties": [
        "Ram Kumar Singh (Plaintiff)",
        "Priya Sharma (Defendant)"
      ],
      "status": "ongoing|closed",
      "filed_date": "2024-05-10",
      "last_hearing_date": "2026-02-28",
      "next_hearing_date": "2026-04-15",
      "case_description": "Detailed description of the case..."
    }
  ]
}
```

#### 5. **FIR (First Information Report)** 🚨 NEW
```json
{
  "fir_details": {
    "fir_number": "FIR-2024-1023",
    "fir_date": "2024-03-15",
    "police_station": "Kisanpur Police Station",
    "offense_section": "Section 406/420/468 IPC - Cheating and dishonest conduct",
    "offense_description": "Fraudulent transfer of land documents and unauthorized possession",
    "filed_by": "Ram Kumar Singh",
    "investigating_officer": "SI Ramesh Kumar",
    "status": "Under Investigation|Closed|Chargesheet Filed"
  }
}
```

#### 6. **Documents** 📎
```json
{
  "documents": [
    {
      "title": "FIR - Land Dispute",
      "document_type": "FIR|Petition|Deed|Survey Report|RTC|Order|Judgment",
      "date": "2024-03-15",
      "url": "https://example.com/docs/document.pdf"
    }
  ]
}
```

#### 7. **Source Information** 📌
```json
{
  "source": {
    "name": "District Court Portal",
    "url": "https://court.example.gov/cases/C123/2024",
    "retrieved_at": "2026-03-04T10:00:00Z"
  }
}
```

---

## 📊 Complete Example - Full Upload

```json
{
  "village": "Kisanpur",
  "survey_number": "123",
  "coordinates": "28.7041,77.1025",
  "location": {
    "latitude": 28.7041,
    "longitude": 77.1025,
    "exact_location": "Near Kisanpur Primary School, Main Road",
    "district": "Bhoomi",
    "state": "Telangana",
    "pin_code": "500001"
  },
  "area_sqft": 4500,
  "area_acres": 0.103,
  "property_type": "Agricultural Land",
  "land_file": {
    "mutation_number": "MUT-2020-1234",
    "original_owner": "Hari Ram Singh",
    "owner_since": "1995",
    "transfer_history": [
      {
        "from": "Hari Ram Singh",
        "to": "Ram Kumar Singh",
        "date": "2015-06-20",
        "deed_number": "DEED-2015-5678"
      }
    ],
    "rtc_number": "RTC-2024-9876",
    "pattadar_passbook": "PPB-123-2024",
    "land_registration_certificate": "LRC-123/2015"
  },
  "linked_cases": [
    {
      "case_id": "C123/2024",
      "case_number": "OS.NO.234/2024",
      "court": "District Court - Bhoomi",
      "bench": "Civil Division - I",
      "case_type": "Original Suit - Land Dispute",
      "parties": [
        "Ram Kumar Singh (Plaintiff)",
        "Priya Sharma (Defendant)"
      ],
      "status": "ongoing",
      "filed_date": "2024-05-10",
      "last_hearing_date": "2026-02-28",
      "next_hearing_date": "2026-04-15",
      "case_description": "Suit for ownership and recovery of possession of disputed agricultural land.",
      "fir_details": {
        "fir_number": "FIR-2024-1023",
        "fir_date": "2024-03-15",
        "police_station": "Kisanpur Police Station",
        "offense_section": "Section 406/420/468 IPC - Cheating and dishonest conduct",
        "offense_description": "Fraudulent transfer of land documents and unauthorized possession",
        "filed_by": "Ram Kumar Singh",
        "investigating_officer": "SI Ramesh Kumar",
        "status": "Under Investigation"
      },
      "documents": [
        {
          "title": "FIR - Land Dispute",
          "document_type": "FIR",
          "date": "2024-03-15",
          "url": "https://example.com/docs/C123_2024_fir.pdf"
        },
        {
          "title": "Petition for Ownership",
          "document_type": "Petition",
          "date": "2024-05-10",
          "url": "https://example.com/docs/C123_2024_petition.pdf"
        },
        {
          "title": "Land Revenue Survey Report",
          "document_type": "Survey Report",
          "date": "2024-04-05",
          "url": "https://example.com/docs/C123_2024_survey.pdf"
        }
      ],
      "source": {
        "name": "District Court Portal",
        "url": "https://court.example.gov/cases/C123/2024",
        "retrieved_at": "2026-03-04T10:00:00Z"
      }
    }
  ]
}
```

---

## 🚀 How to Upload

### **Method 1: Web Admin Panel** (Easiest) ✅
1. Visit: http://localhost:8000/static/admin.html
2. Token: `devtoken123`
3. Paste JSON in textarea (template pre-filled)
4. Click "Upload"

### **Method 2: cURL Command**
```bash
curl -X POST http://localhost:8000/api/v1/admin/upload \
  -H "Authorization: Bearer devtoken123" \
  -H "Content-Type: application/json" \
  -d '{
    "village": "YourVillage",
    "survey_number": "123",
    "property_type": "Agricultural Land",
    "area_sqft": 5000,
    "coordinates": "28.7041,77.1025",
    "location": {
      "latitude": 28.7041,
      "longitude": 77.1025,
      "exact_location": "Main Road Area",
      "district": "Bhoomi",
      "state": "Telangana",
      "pin_code": "500001"
    }
  }'
```

### **Method 3: PowerShell**
```powershell
$data = @{
    village = "YourVillage"
    survey_number = "123"
    property_type = "Agricultural Land"
    area_sqft = 5000
    coordinates = "28.7041,77.1025"
    location = @{
        latitude = 28.7041
        longitude = 77.1025
        exact_location = "Main Road Area"
        district = "Bhoomi"
        state = "Telangana"
        pin_code = "500001"
    }
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/v1/admin/upload" `
  -Headers @{"Authorization"="Bearer devtoken123"; "Content-Type"="application/json"} `
  -Method Post `
  -Body $data
```

---

## 📌 Field Types & Valid Values

| Field | Type | Valid Values | Example |
|-------|------|--------------|---------|
| `village` | String | Village name | "Kisanpur" |
| `survey_number` | String/Number | Survey plot number | "123" |
| `property_type` | String | Agricultural, Residential, Commercial, Industrial, Mixed, Green Belt | "Agricultural Land" |
| `status` (case) | String | "ongoing", "closed", "pending" | "ongoing" |
| `coordinates` | String | "latitude,longitude" | "28.7041,77.1025" |
| `fir_date` | String | ISO 8601 date | "2024-03-15" |
| `filed_date` | String | ISO 8601 date | "2024-05-10" |

---

## ✅ Upload Response

**Success (200 OK):**
```json
{
  "status": "ok",
  "message": "Parcel uploaded successfully"
}
```

**Error (400 Bad Request):**
```json
{
  "detail": "Missing village and/or survey_number"
}
```

**Authentication Error (401/403):**
```json
{
  "detail": "Missing admin token" | "Invalid admin token"
}
```

---

## 📍 Search After Upload

1. Go to: http://localhost:8000/
2. Enter Village: "Your Village"
3. Enter Survey: "123"
4. Click "Search"
5. View your uploaded parcel with all details, location, land files, and cases!

---

## 🔄 Bulk Upload Tips

You can upload multiple records one at a time through the admin panel, or:

1. Upload parcel + basic info first
2. Then upload the same parcel with cases added
3. System automatically merges based on village + survey_number

---

**Status**: ✅ Ready for Upload  
**Admin Token**: `devtoken123`  
**Admin Panel URL**: http://localhost:8000/static/admin.html
