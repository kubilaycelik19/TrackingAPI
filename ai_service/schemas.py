from pydantic import BaseModel

# Kullanıcıdan gelen istek modeli

class ReceiptRequest(BaseModel):
    image_url: str

# Kullanıcıya dönülecek cevap modeli

class ReceiptResponse(BaseModel):
    id: int
    status: str
    merchant: str
    total_amount: float

    class Config:
        from_attributes = True # ORM nesnesini Pydantic'e çevirmek için