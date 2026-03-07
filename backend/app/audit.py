import logging
import json
from datetime import datetime
from typing import Optional, Any
from sqlalchemy.orm import Session
from database import AuditLog

# Configure logger
logger = logging.getLogger("audit")
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def log_audit(
    db: Session,
    actor: str,
    action: str,
    entity_type: str,
    entity_id: str,
    old_value: Optional[dict] = None,
    new_value: Optional[dict] = None,
    ip_address: Optional[str] = None
) -> None:
    """Log audit event to database and console."""
    try:
        audit_entry = AuditLog(
            actor=actor,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            old_value=old_value,
            new_value=new_value,
            ip_address=ip_address,
            created_at=datetime.utcnow()
        )
        db.add(audit_entry)
        db.commit()
        
        # Also log to console
        logger.info(f"AUDIT: {actor} performed {action} on {entity_type}#{entity_id} from {ip_address}")
    except Exception as e:
        logger.error(f"Failed to log audit: {e}")
        db.rollback()


def get_audit_logs(db: Session, limit: int = 100) -> list:
    """Retrieve recent audit logs."""
    return db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit).all()


def export_audit_logs(db: Session) -> str:
    """Export audit logs as JSON."""
    logs = get_audit_logs(db, limit=10000)
    data = [
        {
            "id": log.id,
            "actor": log.actor,
            "action": log.action,
            "entity_type": log.entity_type,
            "entity_id": log.entity_id,
            "created_at": log.created_at.isoformat() if log.created_at else None,
            "ip_address": log.ip_address
        }
        for log in logs
    ]
    return json.dumps(data, indent=2, default=str)
