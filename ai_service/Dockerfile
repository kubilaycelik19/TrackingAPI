FROM python:3.10-slim
WORKDIR /app

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-tur \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# --- 2. PYTHON BAĞIMLILIKLARI ---
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- 3. KODLARI KOPYALA VE BAŞLAT ---
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]