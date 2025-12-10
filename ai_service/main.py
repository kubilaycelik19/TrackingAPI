from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database

# 1. Tabloları oluştur (Migration gibi. Basit yöntem)
# Artık alembic kullanılacağı için yorum satırı yapıldı. Artık 'alembic upgrade' komutu ile tablolar oluşacak.
#models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# 2. Veritabanı Oturumu Sağlayıcı (Dependency Injection)
# Her istekte DB açar, iş bitince kapatır.
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "AI Service with Memory! 🧠"}

# 3. Analiz Endpoint'i
@app.post("/analyze/", response_model=schemas.ReceiptResponse)
def analyze_receipt(request: schemas.ReceiptRequest, db: Session = Depends(get_db)):
    """
    1. Gelen resmi al.
    2. Yapay zeka işlemi yap (Simülasyon).
    3. Sonucu veritabanına kaydet (SQLAlchemy).
    4. Kaydedilen veriyi dön.
    """
    
    # --- AI İŞLEMLERİ (SİMÜLASYON) ---
    # Tesseract OCR veya OpenAI API gelecek.
    simulated_data = {
        "merchant": "Migros",
        "total_amount": 185.50,
        "detected_date": "2025-12-10"
    }
    
    # --- VERİTABANI KAYDI (SQLAlchemy) ---
    # Yeni bir satır oluşturma
    new_log = models.ReceiptLog(
        image_url=request.image_url,
        merchant=simulated_data["merchant"],
        total_amount=simulated_data["total_amount"],
        detected_date=simulated_data["detected_date"]
    )
    
    db.add(new_log)      # Ekle
    db.commit()          # Onayla
    db.refresh(new_log)  # ID'si oluşmuş halini geri çek
    
    # --- CEVAP DÖN ---
    return {
        "id": new_log.id,
        "status": "success",
        "merchant": new_log.merchant,
        "total_amount": new_log.total_amount
    }