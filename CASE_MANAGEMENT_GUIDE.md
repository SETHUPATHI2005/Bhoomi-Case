# Case Management Guide - Delete & Update Cases

## Overview

Your admin panel now supports full case management with three core operations:
- ✅ **View** - List all uploaded cases
- ✏️ **Update** - Modify case details
- 🗑️ **Delete** - Remove cases

---

## Quick Start

### Admin Token
**Token:** `devtoken123`

### Admin Panel URL
Access the case management interface at: **[http://localhost:8000/static/admin.html](http://localhost:8000/static/admin.html)**

---

## 1. Loading All Cases

### Via Web UI

1. Go to admin panel
2. Enter your admin token: `devtoken123`
3. Scroll to **"Manage Cases"** section
4. Click **"Load All Cases"** button
5. All cases from uploaded parcels will appear in a list

### Via API (cURL)
```bash
curl -X GET http://localhost:8000/api/v1/admin/cases \
  -H "X-Admin-Token: devtoken123"
```

### Via API (PowerShell)
```powershell
$headers = @{"X-Admin-Token" = "devtoken123"}
$response = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/admin/cases" -Headers $headers
$response.Content | ConvertFrom-Json
```

### Response Example
```json
{
  "count": 3,
  "cases": [
    {
      "case_id": "C123/2024",
      "village": "Kisanpur",
      "survey_number": "123",
      "court": "District Court - Bhoomi",
      "case_type": "Land Dispute",
      "status": "ongoing",
      "case_number": "OS.NO.123/2024"
    },
    {
      "case_id": "C456/2024",
      "village": "Rajendranagar",
      "survey_number": "456",
      "court": "High Court",
      "case_type": "Boundary Dispute",
      "status": "pending",
      "case_number": "OS.NO.456/2024"
    }
  ]
}
```

---

## 2. Updating a Case

### Via Web UI (Easiest)

1. Load all cases (see above)
2. Find the case you want to edit
3. Click the **"Edit"** button (blue button with pencil icon)
4. A modal window opens with the case data in JSON format
5. Modify the case fields as needed
6. Click **"Save Changes"** button
7. The case is updated and the list refreshes automatically

### Case Fields You Can Update

```json
{
  "case_id": "C123/2024",
  "case_number": "OS.NO.123/2024",
  "court": "District Court - Bhoomi",
  "bench": "Civil Division - I",
  "case_type": "Original Suit - Land Dispute",
  "parties": ["Ram Kumar Singh", "Priya Sharma"],
  "status": "ongoing",  // Can change to: pending, closed, adjourned, disposed
  "filed_date": "2024-01-15",
  "last_hearing_date": "2026-03-01",
  "next_hearing_date": "2026-05-15",
  "case_description": "Description of the case",
  "documents": [
    {
      "title": "FIR Copy",
      "document_type": "FIR",
      "date": "2023-12-20",
      "url": "https://example.com/fir.pdf"
    }
  ],
  "fir_details": {
    "fir_number": "FIR-2024-1023",
    "fir_date": "2023-12-20",
    "police_station": "Kisanpur Police Station",
    "offense_section": "Section 406/420/468 IPC",
    "offense_description": "Fraudulent land transfer",
    "filed_by": "Ram Kumar Singh",
    "investigating_officer": "Inspector Sharma",
    "status": "Under Investigation"
  }
}
```

### Via API (cURL)
```bash
curl -X PUT http://localhost:8000/api/v1/admin/cases/C123%2F2024 \
  -H "X-Admin-Token: devtoken123" \
  -H "Content-Type: application/json" \
  -d '{
    "case_id": "C123/2024",
    "court": "District Court - Bhoomi",
    "status": "closed",
    "case_type": "Land Dispute - Resolved"
  }'
```

### Via API (PowerShell)
```powershell
$caseData = @{
    case_id = "C123/2024"
    status = "closed"
    court = "District Court Updated"
} | ConvertTo-Json

$headers = @{
    "X-Admin-Token" = "devtoken123"
    "Content-Type" = "application/json"
}

$response = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/admin/cases/C123%2F2024" `
    -Method PUT `
    -Headers $headers `
    -Body $caseData

$response.Content | ConvertFrom-Json
```

### Update Response
```json
{
  "status": "ok",
  "message": "Case C123/2024 updated successfully"
}
```

### Common Update Scenarios

**Scenario 1: Change Case Status**
```json
{
  "case_id": "C123/2024",
  "status": "closed"
}
```

**Scenario 2: Update Hearing Dates**
```json
{
  "case_id": "C123/2024",
  "last_hearing_date": "2026-03-15",
  "next_hearing_date": "2026-06-01"
}
```

**Scenario 3: Update FIR Details**
```json
{
  "case_id": "C123/2024",
  "fir_details": {
    "fir_number": "FIR-2024-1023",
    "status": "Investigation Complete",
    "investigating_officer": "Inspector Singh",
    "offense_section": "Section 406/420/468 IPC"
  }
}
```

**Scenario 4: Add New Documents**
```json
{
  "case_id": "C123/2024",
  "documents": [
    {
      "title": "Court Judgment",
      "document_type": "Judgment",
      "date": "2026-03-01",
      "url": "https://court.example.gov/judgment/C123-2024.pdf"
    }
  ]
}
```

---

## 3. Deleting a Case

### Via Web UI (Easiest)

1. Load all cases
2. Find the case you want to delete
3. Click the **"Delete"** button (red button with trash icon)
4. Confirm the deletion in the popup dialog
5. Case is permanently removed

### Via API (cURL)
```bash
curl -X DELETE http://localhost:8000/api/v1/admin/cases/C123%2F2024 \
  -H "X-Admin-Token: devtoken123"
```

### Via API (PowerShell)
```powershell
$headers = @{"X-Admin-Token" = "devtoken123"}
$response = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/admin/cases/C123%2F2024" `
    -Method DELETE `
    -Headers $headers

$response.Content | ConvertFrom-Json
```

### Delete Response
```json
{
  "status": "ok",
  "message": "Case C123/2024 deleted successfully"
}
```

### Important Notes on Deletion

⚠️ **Deletion is permanent** - Deleted cases cannot be recovered
✅ The case is removed from the parcel's `linked_cases` array
✅ The parcel itself remains intact
✅ Other cases in the same parcel are not affected

---

## 4. API Reference

### Endpoints

| Method | Endpoint | Purpose | Auth |
|--------|----------|---------|------|
| GET | `/api/v1/admin/cases` | List all cases | Required |
| GET | `/api/v1/cases/{case_id}` | Get case details | None |
| PUT | `/api/v1/admin/cases/{case_id}` | Update case | Required |
| DELETE | `/api/v1/admin/cases/{case_id}` | Delete case | Required |

### Authentication

All admin operations require the token `devtoken123`:

**Option 1: Header (Recommended)**
```
X-Admin-Token: devtoken123
```

**Option 2: Bearer Token**
```
Authorization: Bearer devtoken123
```

### Case ID Format

Case IDs may contain special characters (/, -, etc). When using in URLs, encode them:

| Case ID | URL Encoded |
|---------|------------|
| C123/2024 | C123%2F2024 |
| C-456/2024 | C-456%2F2024 |
| TEST-999/2024 | TEST-999%2F2024 |

---

## 5. Error Handling

### Common Errors

**401 - Unauthorized (Missing Token)**
```json
{"detail": "Missing admin token"}
```
**Solution:** Add `X-Admin-Token` header with value `devtoken123`

**403 - Forbidden (Invalid Token)**
```json
{"detail": "Invalid admin token"}
```
**Solution:** Verify token is exactly `devtoken123`

**404 - Case Not Found**
```json
{"detail": "Case not found"}
```
**Solution:** 
- Verify case_id is correct
- Make sure the case exists (check with GET /api/v1/admin/cases)
- URL-encode special characters properly

**400 - Bad Request (Invalid JSON)**
```json
{"detail": "Expected JSON object"}
```
**Solution:** Verify JSON syntax is valid. Use online JSON validator if needed.

**500 - Server Error**
```json
{"detail": "Update failed"}
```
**Solution:** Check server logs and verify case structure is valid

---

## 6. Workflow Examples

### Example: Resolving a Disputed Case

**Step 1:** List all cases
```bash
curl -X GET http://localhost:8000/api/v1/admin/cases \
  -H "X-Admin-Token: devtoken123"
```

**Step 2:** Find case "C123/2024" and update its status
```bash
curl -X PUT http://localhost:8000/api/v1/admin/cases/C123%2F2024 \
  -H "X-Admin-Token: devtoken123" \
  -H "Content-Type: application/json" \
  -d '{
    "case_id": "C123/2024",
    "status": "closed",
    "case_description": "Case resolved in favor of plaintiff",
    "last_hearing_date": "2026-03-20"
  }'
```

**Step 3:** Verify update
```bash
curl http://localhost:8000/api/v1/cases/C123%2F2024
```

### Example: Removing Duplicate Cases

**Step 1:** Load all cases to identify duplicates
```bash
curl -X GET http://localhost:8000/api/v1/admin/cases \
  -H "X-Admin-Token: devtoken123"
```

**Step 2:** Delete the duplicate
```bash
curl -X DELETE http://localhost:8000/api/v1/admin/cases/DUPLICATE-ID%2F2024 \
  -H "X-Admin-Token: devtoken123"
```

### Example: Bulk Update Status

Update multiple cases from "ongoing" to "closed":

```bash
# Get all cases
cases=$(curl -s http://localhost:8000/api/v1/admin/cases \
  -H "X-Admin-Token: devtoken123" | jq '.cases')

# For each case with status "ongoing", update to "closed"
echo "$cases" | jq '.[] | select(.status=="ongoing") | .case_id' | while read caseId; do
  curl -X PUT http://localhost:8000/api/v1/admin/cases/${caseId//\"} \
    -H "X-Admin-Token: devtoken123" \
    -H "Content-Type: application/json" \
    -d '{"status": "closed"}'
done
```

---

## 7. Data Persistence

📁 **Storage Location:** `backend/app/data/admin_uploads.json`

- All updates and deletions are persisted to this file
- Changes survive server restarts
- Manual backups recommended before bulk deletions
- File format: JSON array of parcels with linked_cases

---

## 8. Tips & Best Practices

✅ **DO:**
- Backup your data before bulk updates
- Use URL encoding for special characters
- Test updates with a single case first
- Verify JSON syntax before uploading
- Keep detailed records of case changes

❌ **DON'T:**
- Share admin token publicly
- Delete cases without confirmation
- Modify case_id field (create new case instead)
- Store sensitive info outside encrypted channels
- Update live cases during active proceedings

---

## Support

For issues or questions:
1. Check the error message carefully
2. Verify admin token is correct
3. Ensure JSON syntax is valid
4. Check case_id encoding
5. Review server logs

