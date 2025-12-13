from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import models, database
from ocr import perform_ocr 

# Tabloları oluştur
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "AI Service is Running (File Upload Mode) 🚀"}

@app.post("/analyze/")
async def analyze_receipt(file: UploadFile = File(...), db: Session = Depends(get_db)):
    
    print(f"Dosya Alındı: {file.filename}")

    # Dosya içeriği okuma
    image_data = await file.read()

    # OCR İşlemi
    extracted_data = perform_ocr(image_data)
    
    if not extracted_data:
        raise HTTPException(status_code=400, detail="OCR işlemi başarısız oldu.")
    
    print(f"OCR Sonucu: {extracted_data}")

    # 3. DB Loglama
    # Dosya adını kaydetme
    new_log = models.ReceiptLog(
        image_url=f"file://{file.filename}", 
        merchant=extracted_data["merchant"],
        total_amount=extracted_data["total_amount"],
        detected_date=extracted_data["detected_date"]
    )
    
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    
    return {
        "status": "success",
        "merchant": new_log.merchant,
        "total_amount": new_log.total_amount,
        "detected_date": new_log.detected_date
    }