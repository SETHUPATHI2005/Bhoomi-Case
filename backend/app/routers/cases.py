"""Public cases / search router — /api/v1/search, /api/v1/cases endpoints."""
import logging

from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from app.services.case_service import load_admin_uploads, load_data, normalize

router = APIRouter(tags=["cases"])
logger = logging.getLogger("router.cases")

from datetime import datetime
import uuid
from fastapi import Request, Depends, File, UploadFile, Form
from app.dependencies import get_current_user
from app.services.case_service import load_citizen_submissions, save_citizen_submissions, save_upload_file

@router.post("/cases/submit")
async def submit_case(
    request: Request,
    village: str = Form(...),
    survey_number: str = Form(...),
    property_type: str = Form("Unknown"),
    area_sqft: str = Form(""),
    area_acres: str = Form(""),
    coordinates: str = Form(""),
    # Location
    address: str = Form(""),
    district: str = Form(""),
    state: str = Form(""),
    pin_code: str = Form(""),
    # Land Records
    owner_original: str = Form(""),
    owner_current: str = Form(""),
    owner_since: str = Form(""),
    doc_mutation: str = Form(""),
    doc_rtc: str = Form(""),
    doc_passbook: str = Form(""),
    lrc: str = Form(""),
    # Case Info
    court: str = Form(""),
    bench: str = Form(""),
    case_type: str = Form("General"),
    case_number: str = Form(""),
    filed_date: str = Form(""),
    next_hearing_date: str = Form(""),
    case_description: str = Form(""),
    # Parties
    plaintiff: str = Form(""),
    defendant: str = Form(""),
    # FIR
    fir_number: str = Form(""),
    fir_date: str = Form(""),
    fir_station: str = Form(""),
    fir_status: str = Form(""),
    fir_section: str = Form(""),
    fir_offense: str = Form(""),
    fir_filed_by: str = Form(""),
    fir_io: str = Form(""),
    # Files
    case_doc: Optional[UploadFile] = File(None),
    fir_doc: Optional[UploadFile] = File(None),
    land_doc: Optional[UploadFile] = File(None),
    survey_doc: Optional[UploadFile] = File(None),
    rtc_doc: Optional[UploadFile] = File(None),
    mutation_doc: Optional[UploadFile] = File(None),
    current_user: dict = Depends(get_current_user)
):
    """Citizens submit a case for admin verification with document uploads."""
    try:
        submission_id = str(uuid.uuid4())
        
        # Save uploaded files
        case_doc_path = await save_upload_file(case_doc, sub_directory=submission_id)
        fir_doc_path = await save_upload_file(fir_doc, sub_directory=submission_id)
        land_doc_path = await save_upload_file(land_doc, sub_directory=submission_id)
        survey_doc_path = await save_upload_file(survey_doc, sub_directory=submission_id)
        rtc_doc_path = await save_upload_file(rtc_doc, sub_directory=submission_id)
        mutation_doc_path = await save_upload_file(mutation_doc, sub_directory=submission_id)

        # Build parties list
        parties = []
        if plaintiff:
            parties.append(f"{plaintiff} (Plaintiff)")
        if defendant:
            parties.append(f"{defendant} (Defendant)")
            
        submission = {
            "submission_id": submission_id,
            "village": village,
            "survey_number": survey_number,
            "property_type": property_type,
            "area_sqft": int(area_sqft) if area_sqft else None,
            "area_acres": float(area_acres) if area_acres else None,
            "coordinates": coordinates,
            "case_id": f"SB-{submission_id[:8].upper()}",
            "status": "pending_verification",
            "submitted_by": current_user.get("username"),
            "submitted_at": datetime.now().isoformat(),
            "location": {
                "exact_location": address,
                "district": district,
                "state": state,
                "pin_code": pin_code
            },
            "land_file": {
                "mutation_number": doc_mutation,
                "original_owner": owner_original,
                "owner_since": owner_since,
                "rtc_number": doc_rtc,
                "pattadar_passbook": doc_passbook,
                "land_registration_certificate": lrc,
                "transfer_history": [{
                    "from": owner_original,
                    "to": owner_current,
                    "date": filed_date
                }] if owner_original and owner_current else []
            },
            "linked_cases": [{
                "case_id": f"SB-{submission_id[:8].upper()}",
                "case_number": case_number,
                "court": court or "Pending",
                "bench": bench,
                "case_type": case_type,
                "status": "ongoing",
                "filed_date": filed_date,
                "next_hearing_date": next_hearing_date,
                "case_description": case_description,
                "parties": parties,
                "fir_details": {
                    "fir_number": fir_number,
                    "fir_date": fir_date,
                    "police_station": fir_station,
                    "status": fir_status,
                    "offense_section": fir_section,
                    "offense_description": fir_offense,
                    "filed_by": fir_filed_by,
                    "investigating_officer": fir_io,
                    "file_path": fir_doc_path
                },
                "documents": []
            }],
            "ownership_details": {
                "original_owner": owner_original,
                "current_owner": owner_current
            },
            "document_paths": {
                "case_doc": case_doc_path,
                "fir_doc": fir_doc_path,
                "land_doc": land_doc_path,
                "survey_doc": survey_doc_path,
                "rtc_doc": rtc_doc_path,
                "mutation_doc": mutation_doc_path,
            }
        }
        
        # Build documents list from uploaded files
        doc_entries = []
        if case_doc_path:
            doc_entries.append({"title": "Primary Case Document", "document_type": "Case Document", "url": case_doc_path})
        if fir_doc_path:
            doc_entries.append({"title": "FIR Document", "document_type": "FIR", "url": fir_doc_path})
        if land_doc_path:
            doc_entries.append({"title": "Land Document", "document_type": "Land Record", "url": land_doc_path})
        if survey_doc_path:
            doc_entries.append({"title": "Land Revenue Survey Report", "document_type": "Survey Report", "url": survey_doc_path})
        if rtc_doc_path:
            doc_entries.append({"title": "RTC Certificate", "document_type": "Revenue Record", "url": rtc_doc_path})
        if mutation_doc_path:
            doc_entries.append({"title": "Mutation Deed Document", "document_type": "Land Record", "url": mutation_doc_path})
        submission["linked_cases"][0]["documents"] = doc_entries
        
        subs = load_citizen_submissions()
        subs.append(submission)
        save_citizen_submissions(subs)
        
        logger.info(f"User {current_user.get('username')} submitted a case with files for {village} {survey_number}")
        return JSONResponse(status_code=201, content={
            "status": "ok", 
            "message": "Case submitted successfully! It is pending admin verification.",
            "submission_id": submission["submission_id"]
        })
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Submit case error: {e}")
        raise HTTPException(status_code=500, detail="Submission failed")



@router.get("/search")
async def search(
    village: str = Query(..., min_length=1),
    survey: str = Query(..., min_length=1),
):
    """Search parcels by village and survey number."""
    try:
        nv = normalize(village)
        ns = normalize(survey)
        parcels = load_data() + load_admin_uploads()
        results = [
            p for p in parcels
            if normalize(p.get("village", "")) == nv and normalize(p.get("survey_number", "")) == ns
        ]
        return JSONResponse(content={"count": len(results), "results": results})
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail="Search failed")


@router.get("/parcels")
async def get_parcels(village: str = Query(...), survey: str = Query(...)):
    """Alias for /api/v1/search."""
    return await search(village=village, survey=survey)


@router.get("/cases/{case_id:path}")
async def get_case(case_id: str):
    """Retrieve a single case by its case_id."""
    try:
        parcels = load_data() + load_admin_uploads()
        for p in parcels:
            for c in p.get("linked_cases", []):
                if c.get("case_id") == case_id:
                    return JSONResponse(content=c)
        raise HTTPException(status_code=404, detail="Case not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get case error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch case")
