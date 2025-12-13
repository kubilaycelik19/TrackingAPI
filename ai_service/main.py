from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database
from ocr import perform_ocr 

# Tabloları oluştur
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Veritabanı oturumu
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "AI Service is Running with Tesseract! 👁️"}

@app.post("/analyze/", response_model=schemas.ReceiptResponse)
def analyze_receipt(request: schemas.ReceiptRequest, db: Session = Depends(get_db)):
    
    print(f"Analiz Başlıyor: {request.image_url}") # Loglama işlemi

    extracted_data = perform_ocr(request.image_url)
    
    # Eğer OCR bir şekilde hata verir veya boş dönerse
    if not extracted_data:
        raise HTTPException(status_code=400, detail="OCR işlemi başarısız oldu veya resim okunamadı.")
    
    print(f"OCR Sonucu: {extracted_data}") # Loglama

    # --- VERİTABANI KAYDI ---
    new_log = models.ReceiptLog(
        image_url=request.image_url,
        merchant=extracted_data["merchant"],
        total_amount=extracted_data["total_amount"],
        detected_date=extracted_data["detected_date"]
    )
    
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    
    # --- CEVAP DÖN ---
    return {
        "id": new_log.id,
        "status": "success",
        "merchant": new_log.merchant,
        "total_amount": new_log.total_amount
    }