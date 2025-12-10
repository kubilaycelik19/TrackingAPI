from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database import Base

class ReceiptLog(Base):
    __tablename__ = "receipt_logs"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, index=True)
    merchant = Column(String)
    total_amount = Column(Float)
    detected_date = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)