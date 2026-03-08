"""Admin case management router — /api/v1/admin/ case endpoints."""
import logging
import json
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, File, UploadFile, Form
from fastapi.responses import JSONResponse

from app.dependencies import verify_admin
from app.services.case_service import (
    find_case_in_parcel,
    load_admin_uploads,
    save_admin_uploads,
    load_citizen_submissions,
    save_citizen_submissions,
    save_upload_file,
)

router = APIRouter(tags=["admin-cases"])
logger = logging.getLogger("router.admin_cases")

@router.get("/submissions")
async def list_submissions(admin_id: str = Depends(verify_admin)):
    """List pending case submissions from citizens."""
    try:
        subs = load_citizen_submissions()
        pending = [s for s in subs if s.get("status") == "pending_verification"]
        return JSONResponse(content={"count": len(pending), "submissions": pending})
    except Exception as e:
        logger.error(f"List submissions error: {e}")
        raise HTTPException(status_code=500, detail="Failed to list submissions")

@router.get("/stats")
async def get_dashboard_stats(admin_id: str = Depends(verify_admin)):
    """Get aggregate statistics for the admin dashboard."""
    try:
        citizen_subs = load_citizen_submissions()
        admin_uploads = load_admin_uploads()
        
        pending_count = len([s for s in citizen_subs if s.get("status") == "pending_verification"])
        
        approved_count = 0
        for parcel in admin_uploads:
            approved_count += len(parcel.get("linked_cases", []))
            
        return JSONResponse(content={
            "total_submissions": len(citizen_subs),
            "pending_verification": pending_count,
            "approved_cases": approved_count
        })
    except Exception as e:
        logger.error(f"Stats error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch stats")

@router.post("/submissions/{sub_id}/approve")
async def approve_submission(sub_id: str, admin_id: str = Depends(verify_admin)):
    """Approve a citizen case submission and add it to the active parcels."""
    try:
        subs = load_citizen_submissions()
        sub = next((s for s in subs if s.get("submission_id") == sub_id), None)
        if not sub:
            raise HTTPException(status_code=404, detail="Submission not found")
        
        if sub.get("status") != "pending_verification":
            raise HTTPException(status_code=400, detail="Submission is not pending")
            
        # Update submission status
        sub["status"] = "verified"
        sub["verified_by"] = admin_id
        save_citizen_submissions(subs)
        
        # Add to admin_uploads
        uploads = load_admin_uploads()
        
        # Find if parcel exists
        village = sub.get("village")
        survey = sub.get("survey_number")
        
        parcel = next((p for p in uploads if p.get("village") == village and p.get("survey_number") == survey), None)
        
        case_data = {
            "case_id": sub.get("case_id"),
            "court": sub.get("court"),
            "case_type": sub.get("case_type"),
            "status": "ongoing",
            "submitted_by": sub.get("submitted_by"),
            "verified_by": admin_id,
            "ownership_details": sub.get("ownership_details", {}),
            "land_documents": sub.get("land_documents", {}),
            "fir_details": sub.get("fir_details", {})
        }
        
        if parcel:
            if "linked_cases" not in parcel:
                parcel["linked_cases"] = []
            parcel["linked_cases"].append(case_data)
        else:
            new_parcel = {
                "village": village,
                "survey_number": survey,
                "property_type": sub.get("property_type", "Unknown"),
                "linked_cases": [case_data]
            }
            uploads.append(new_parcel)
            
        save_admin_uploads(uploads)
        
        logger.info(f"Admin approved submission {sub_id}")
        return JSONResponse(content={"status": "ok", "message": "Submission approved and case added"})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Approve submission error: {e}")
        raise HTTPException(status_code=500, detail="Failed to approve submission")

@router.post("/submissions/{sub_id}/reject")
async def reject_submission(sub_id: str, admin_id: str = Depends(verify_admin)):
    """Reject a citizen case submission."""
    try:
        subs = load_citizen_submissions()
        sub = next((s for s in subs if s.get("submission_id") == sub_id), None)
        if not sub:
            raise HTTPException(status_code=404, detail="Submission not found")
            
        if sub.get("status") != "pending_verification":
            raise HTTPException(status_code=400, detail="Submission is not pending")
            
        sub["status"] = "rejected"
        sub["rejected_by"] = admin_id
        save_citizen_submissions(subs)
        
        logger.info(f"Admin rejected submission {sub_id}")
        return JSONResponse(content={"status": "ok", "message": "Submission rejected"})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Reject submission error: {e}")
        raise HTTPException(status_code=500, detail="Failed to reject submission")

@router.post("/upload-multipart")
async def admin_upload_multipart(
    village: str = Form(...),
    survey_number: str = Form(...),
    property_type: str = Form("Unknown"),
    payload_json: str = Form(None),
    case_doc: Optional[UploadFile] = File(None),
    fir_doc: Optional[UploadFile] = File(None),
    land_doc: Optional[UploadFile] = File(None),
    admin_id: str = Depends(verify_admin)
):
    """Multipart upload for admins with file support."""
    try:
        # Parse payload if provided
        data = {}
        if payload_json:
            try:
                data = json.loads(payload_json)
            except:
                pass
        
        # Override with form fields
        data["village"] = village
        data["survey_number"] = survey_number
        data["property_type"] = property_type
        
        # Save files
        upload_id = str(uuid.uuid4())
        case_doc_path = await save_upload_file(case_doc, sub_directory=upload_id)
        fir_doc_path = await save_upload_file(fir_doc, sub_directory=upload_id)
        land_doc_path = await save_upload_file(land_doc, sub_directory=upload_id)
        
        # Update data with file paths
        if "linked_cases" not in data or not data["linked_cases"]:
            data["linked_cases"] = [{}]
            
        case = data["linked_cases"][0]
        if case_doc_path:
            case["case_document_path"] = case_doc_path
            
        if fir_doc_path:
            if "fir_details" not in case:
                case["fir_details"] = {}
            case["fir_details"]["file_path"] = fir_doc_path
            
        if land_doc_path:
            if "land_file" not in data:
                data["land_file"] = {}
            data["land_file"]["file_path"] = land_doc_path

        uploads = load_admin_uploads()
        uploads.append(data)
        save_admin_uploads(uploads)

        logger.info(f"Admin {admin_id} uploaded multipart: {village} #{survey_number}")
        return JSONResponse(content={"status": "ok", "message": "Parcel and files uploaded successfully"})
    except Exception as e:
        logger.error(f"Multipart upload error: {e}")
        raise HTTPException(status_code=500, detail="Multipart upload failed")

@router.get("/cases")
async def list_all_cases(admin_id: str = Depends(verify_admin)):
    """List all cases from admin uploads."""
    try:
        uploads = load_admin_uploads()
        cases = []
        for parcel in uploads:
            for case in parcel.get("linked_cases", []):
                cases.append({
                    "case_id": case.get("case_id"),
                    "village": parcel.get("village"),
                    "survey_number": parcel.get("survey_number"),
                    "court": case.get("court"),
                    "case_type": case.get("case_type"),
                    "status": case.get("status"),
                    "case_number": case.get("case_number"),
                })
        return JSONResponse(content={"count": len(cases), "cases": cases})
    except Exception as e:
        logger.error(f"List cases error: {e}")
        raise HTTPException(status_code=500, detail="Failed to list cases")

@router.delete("/cases/{case_id:path}")
async def delete_case(case_id: str, admin_id: str = Depends(verify_admin)):
    """Delete a case by case_id."""
    try:
        uploads = load_admin_uploads()
        parcel, case, parcel_idx = find_case_in_parcel(case_id, uploads)
        if parcel is None:
            raise HTTPException(status_code=404, detail="Case not found")

        case_idx = next(
            i for i, c in enumerate(uploads[parcel_idx].get("linked_cases", []))
            if c.get("case_id") == case_id
        )
        uploads[parcel_idx]["linked_cases"].pop(case_idx)
        save_admin_uploads(uploads)

        logger.info(f"Admin {admin_id} deleted case: {case_id}")
        return JSONResponse(content={"status": "ok", "message": f"Case {case_id} deleted successfully"})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete case error: {e}")
        raise HTTPException(status_code=500, detail="Delete failed")

@router.put("/cases/{case_id:path}")
async def update_case(case_id: str, request: Request, admin_id: str = Depends(verify_admin)):
    """Update a case's fields by case_id."""
    try:
        payload = await request.json()
        if not isinstance(payload, dict):
            raise HTTPException(status_code=400, detail="Expected a JSON object")

        uploads = load_admin_uploads()
        parcel, case, parcel_idx = find_case_in_parcel(case_id, uploads)
        if parcel is None:
            raise HTTPException(status_code=404, detail="Case not found")

        for idx, c in enumerate(uploads[parcel_idx].get("linked_cases", [])):
            if c.get("case_id") == case_id:
                payload["case_id"] = case_id  # preserve original ID
                uploads[parcel_idx]["linked_cases"][idx] = payload
                break

        save_admin_uploads(uploads)
        logger.info(f"Admin {admin_id} updated case: {case_id}")
        return JSONResponse(content={"status": "ok", "message": f"Case {case_id} updated successfully"})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update case error: {e}")
        raise HTTPException(status_code=500, detail="Update failed")
