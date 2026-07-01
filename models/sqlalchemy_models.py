from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from datetime import datetime
from ml_service.database.session import Base
import pytz

class DetectionLog(Base):
    __tablename__ = "detection_logs"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    is_phishing = Column(Boolean)
    confidence = Column(Float)
    message = Column(String)
    timestamp = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))