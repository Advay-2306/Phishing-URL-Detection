from ..database.session import SessionLocal
from models.sqlalchemy_models import DetectionLog
from datetime import datetime
import pytz

def log_detection(url: str, is_phishing: bool, confidence: float, message: str):
    db = SessionLocal()
    try:
        log_entry = DetectionLog(
            url=url,
            is_phishing=is_phishing,
            confidence=confidence,
            message=message,
            timestamp=datetime.now(pytz.timezone('Asia/Kolkata'))
        )
        db.add(log_entry)
        db.commit()
    finally:
        db.close()