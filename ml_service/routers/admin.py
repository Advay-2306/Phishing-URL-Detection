from fastapi import APIRouter
from ..database.session import SessionLocal
from models.sqlalchemy_models import DetectionLog
from datetime import datetime
import pytz

router = APIRouter(prefix="/api", tags=["admin"])


@router.get("/logs")
def get_logs(limit: int = 50):
    db = SessionLocal()
    logs = db.query(DetectionLog).order_by(DetectionLog.timestamp.desc()).limit(limit).all()
    db.close()

    for log in logs:
        if log.timestamp:
            log.timestamp = log.timestamp.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Kolkata'))

    return logs

@router.get("/metrics")
def get_metrics():
    db = SessionLocal()
    total = db.query(DetectionLog).count()
    phishing_count = db.query(DetectionLog).filter(DetectionLog.is_phishing == True).count()
    db.close()
    return {
        "total_checks": total,
        "phishing_detected": phishing_count,
        "detection_rate": round(phishing_count / total * 100, 2) if total > 0 else 0
    }