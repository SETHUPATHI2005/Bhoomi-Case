"""
ETL module for ingesting court case and parcel data.
Supports JSON files, CSV, and web scraping.
"""
import json
import csv
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from database import Case, Parcel, Document

logger = logging.getLogger("etl")


def normalize_village_name(name: str) -> str:
    """Normalize village name for consistent matching."""
    if not name:
        return ""
    return "".join(ch for ch in name.lower() if ch.isalnum())


def normalize_survey_number(num: str) -> str:
    """Normalize survey number for consistent matching."""
    if not num:
        return ""
    return "".join(ch for ch in str(num) if ch.isalnum())


def ingest_json_parcels(db: Session, filepath: str) -> int:
    """Ingest parcel data from JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        count = 0
        if isinstance(data, list):
            for item in data:
                parcel = Parcel(
                    village=item.get('village'),
                    survey_number=item.get('survey_number'),
                    linked_case_ids=item.get('linked_cases', []),
                    coordinates=item.get('coordinates')
                )
                db.add(parcel)
                count += 1
        
        db.commit()
        logger.info(f"Ingested {count} parcels from {filepath}")
        return count
    except Exception as e:
        logger.error(f"Failed to ingest parcels from {filepath}: {e}")
        db.rollback()
        return 0


def ingest_json_cases(db: Session, filepath: str) -> int:
    """Ingest case data from JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        count = 0
        if isinstance(data, list):
            for item in data:
                # Check for duplicate
                existing = db.query(Case).filter(Case.case_id == item.get('case_id')).first()
                if existing:
                    logger.debug(f"Case {item.get('case_id')} already exists, skipping")
                    continue
                
                case = Case(
                    case_id=item.get('case_id'),
                    court=item.get('court'),
                    parties=item.get('parties', []),
                    status=item.get('status'),
                    filed_date=item.get('filed_date'),
                    last_hearing_date=item.get('last_hearing_date'),
                    linked_parcel_ids=item.get('linked_parcels', []),
                    source=item.get('source')
                )
                db.add(case)
                count += 1
        
        db.commit()
        logger.info(f"Ingested {count} cases from {filepath}")
        return count
    except Exception as e:
        logger.error(f"Failed to ingest cases from {filepath}: {e}")
        db.rollback()
        return 0


def ingest_csv_parcels(db: Session, filepath: str) -> int:
    """Ingest parcel data from CSV file."""
    try:
        count = 0
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                parcel = Parcel(
                    village=row.get('village'),
                    survey_number=row.get('survey_number'),
                    coordinates=row.get('coordinates')
                )
                db.add(parcel)
                count += 1
        
        db.commit()
        logger.info(f"Ingested {count} parcels from CSV {filepath}")
        return count
    except Exception as e:
        logger.error(f"Failed to ingest CSV parcels: {e}")
        db.rollback()
        return 0


def search_parcels(db: Session, village: str, survey_number: str) -> List[Parcel]:
    """Search for parcels by normalized village and survey number."""
    nv = normalize_village_name(village)
    ns = normalize_survey_number(survey_number)
    
    # Query with normalization in Python (can be optimized with DB functions)
    all_parcels = db.query(Parcel).all()
    results = [
        p for p in all_parcels
        if normalize_village_name(p.village) == nv and normalize_survey_number(p.survey_number) == ns
    ]
    return results


def get_cases_for_parcel(db: Session, parcel_id: int) -> List[Case]:
    """Get all cases linked to a parcel."""
    parcel = db.query(Parcel).filter(Parcel.id == parcel_id).first()
    if not parcel or not parcel.linked_case_ids:
        return []
    
    cases = db.query(Case).filter(Case.id.in_(parcel.linked_case_ids)).all()
    return cases


def link_case_to_parcel(db: Session, case_id: str, parcel_id: int) -> bool:
    """Link a case to a parcel."""
    try:
        case = db.query(Case).filter(Case.case_id == case_id).first()
        parcel = db.query(Parcel).filter(Parcel.id == parcel_id).first()
        
        if not case or not parcel:
            return False
        
        if case.id not in (parcel.linked_case_ids or []):
            parcel.linked_case_ids = parcel.linked_case_ids or []
            parcel.linked_case_ids.append(case.id)
            parcel.updated_at = datetime.utcnow()
            db.commit()
            logger.info(f"Linked case {case_id} to parcel {parcel_id}")
            return True
        return False
    except Exception as e:
        logger.error(f"Failed to link case to parcel: {e}")
        db.rollback()
        return False
