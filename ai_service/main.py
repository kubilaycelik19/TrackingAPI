from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Pydantic modeli gelen verinin tipini doğrular.
class ReceiptAnalysisRequest(BaseModel):
    image_url: str

@app.get("/")
def read_root():
    return {"message": "AI Service is running"}

@app.post("/analyze/")
def analyze_receipt(data: ReceiptAnalysisRequest):
    # Yapay zeka kodları gelecek.
    # Manuel örnek veri.
    return {
        "status": "success",
        "file_processed": data.image_url,
        "extracted_data": {
            "total_amount": 150.00,
            "date": "2025-12-09",
            "merchant": "Migros"
        }
    }