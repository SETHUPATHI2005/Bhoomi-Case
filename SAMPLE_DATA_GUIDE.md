# Bhoomi Court Cases - Sample Data Documentation

## Current Data Summary

### Villages & Parcels Included:

1. **Kisanpur** (5 parcels)
   - Survey 123: Agricultural Land - Case C123/2024 (Ongoing)
   - Survey 124: Mixed Agricultural - Case C124/2023 (Ongoing)
   - Survey 125: Residential - No cases

2. **Rajendranagar** (2 parcels)
   - Survey 201: Industrial Land - Case C201/2024 (Ongoing) - High Court
   - Survey 202: Commercial - Case C202/2023 (Closed)

3. **Tellapur** (3 parcels)
   - Survey 301: Agricultural - Case C301/2024 (Ongoing) - Revenue Court
   - Survey 302: Residential - Case C302/2022 (Closed)
   - Survey 303: Agricultural - No cases

4. **Chevella** (2 parcels)
   - Survey 401: Agricultural - Case C401/2024 (Ongoing)
   - Survey 402: Green Belt - No cases

5. **Villachetty** (1 parcel)
   - Survey 501: Commercial - Case C501/2024 (Ongoing)

### Total: 13 Parcels with 9 Active/Closed Cases

---

## Case Types Represented:

- **Boundary Disputes** (Kisanpur 124)
- **Land Ownership Disputes** (Kisanpur 123, Tellapur 301)
- **Environmental/Industrial** (Rajendranagar 201)
- **Commercial Disputes** (Rajendranagar 202, Villachetty 501)
- **Settled Cases** (Tellapur 302, Rajendranagar 202)

---

## Court Systems Included:

1. **District Court - Bhoomi** (Primary court for most cases)
2. **High Court - Hyderabad** (Appellate cases)
3. **Revenue Court - Bhoomi** (Land revenue disputes)

---

## Document Types in Sample Data:

- FIR (First Information Report)
- Petitions & Writ Petitions
- Survey Reports
- Property Deeds
- Court Orders & Judgments
- Environmental Impact Reports
- Municipal Objections
- Boundary Dispute Reports
- Settlement Agreements
- RTC Documents (Revenue/Tahsildar)
- Pattadar Pass Book
- Land Registration Certificates
- Site Inspection Reports
- Loan Agreements
- Property Valuation Reports
- Foreclosure Notices
- Execution Petitions

---

## Data Fields in Each Parcel Record:

```json
{
  "id": "unique_identifier",
  "village": "Village Name",
  "survey_number": "Survey Number",
  "coordinates": "latitude,longitude",
  "area_sqft": 5000,
  "property_type": "Type of property",
  "linked_cases": [
    {
      "case_id": "CaseNumber/Year",
      "court": "Court Name",
      "parties": ["Party 1", "Party 2"],
      "status": "ongoing|closed",
      "filed_date": "YYYY-MM-DD",
      "last_hearing_date": "YYYY-MM-DD",
      "next_hearing_date": "YYYY-MM-DD (if ongoing)",
      "documents": [
        {
          "title": "Document Title",
          "url": "Document URL"
        }
      ],
      "source": {
        "name": "Source Portal Name",
        "url": "Portal URL",
        "retrieved_at": "ISO 8601 Timestamp"
      }
    }
  ]
}
```

---

## How to Add More Data:

### Via Admin Panel:
1. Visit: http://localhost:8000/static/admin.html
2. Enter your admin token: `devtoken123`
3. Paste JSON in Parcel Data field
4. Click Upload

### Example Parcel JSON:
```json
{
  "village": "Your Village",
  "survey_number": "123",
  "coordinates": "28.5041,77.3025",
  "area_sqft": 5000,
  "property_type": "Agricultural Land",
  "linked_cases": []
}
```

### Example Parcel with Cases:
```json
{
  "village": "Your Village",
  "survey_number": "456",
  "coordinates": "28.5045,77.3030",
  "area_sqft": 6000,
  "property_type": "Commercial",
  "linked_cases": [
    {
      "case_id": "C456/2024",
      "court": "District Court - Bhoomi",
      "parties": ["Party A", "Party B"],
      "status": "ongoing",
      "filed_date": "2024-01-15",
      "last_hearing_date": "2026-03-01",
      "next_hearing_date": "2026-04-15",
      "documents": [
        {
          "title": "Petition",
          "url": "https://example.com/documents/C456_petition.pdf"
        }
      ],
      "source": {
        "name": "District Court Portal",
        "url": "https://court.example.gov/cases/C456/2024",
        "retrieved_at": "2026-03-04T10:00:00Z"
      }
    }
  ]
}
```

---

## Searching the Data:

### Try these searches:
- **Village**: Kisanpur, Rajendranagar, Tellapur, Chevella, Villachetty
- **Survey Numbers**:
  - Kisanpur: 123, 124, 125
  - Rajendranagar: 201, 202
  - Tellapur: 301, 302, 303
  - Chevella: 401, 402
  - Villachetty: 501

---

## Property Types:
- Agricultural Land
- Mixed Agricultural
- Residential Plot
- Commercial Plot
- Industrial Land
- Green Belt

---

## Status Types:
- **Ongoing**: Case is currently active in court
- **Closed**: Case has been disposed/decided
- **Pending**: Case awaiting next hearing

---

Last Updated: March 4, 2026
Total Records: 13 Parcels | 9 Court Cases
