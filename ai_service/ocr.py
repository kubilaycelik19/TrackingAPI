import pytesseract
from PIL import Image, ImageEnhance
from io import BytesIO
import re
from collections import Counter

def perform_ocr(image_bytes: bytes):
    try:

        image = Image.open(BytesIO(image_bytes))
        
        # --- GÖRÜNTÜ İYİLEŞTİRME ---
        image = image.convert('L') # Siyah Beyaz
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0) # Kontrast artırma
        
        # Tesseract okuması
        raw_text = pytesseract.image_to_string(image, lang='tur')
        
        return parse_receipt_text(raw_text)
    except Exception as e:
        print(f"OCR Hatası: {e}")
        return None

def parse_receipt_text(text):
    # Loglama (Ham veri)
    print("\n" + "="*30)
    print("HAM METİN:")
    print(text)
    print("="*30 + "\n")

    data = {
        "merchant": "Bilinmiyor",
        "total_amount": 0.0,
        "detected_date": "2025-01-01"
    }
    
    lines = text.split('\n')
    
    # --- İŞYERİ ADI ---
    for line in lines:
        clean = line.strip()
        if len(clean) > 3 and not clean.replace(' ', '').isdigit():
            if "TEŞEKKÜR" in clean.upper() or "TOPLAM" in clean.upper():
                continue
            data["merchant"] = clean
            break

    # --- TARİH ---
    date_match = re.search(r'(\d{2}[./]\d{2}[./]\d{4})', text)
    if date_match:
        raw_date = date_match.group(1)
        formatted = raw_date.replace('/', '-').replace('.', '-')
        parts = formatted.split('-')
        if len(parts) == 3:
            data["detected_date"] = f"{parts[2]}-{parts[1]}-{parts[0]}"

    # --- TOPLAM TUTAR ---
    clean_text_for_price = text.replace(' ', '')
    matches = re.findall(r'(\d+[.,]\d{2})', clean_text_for_price)
    
    found_prices = []
    for match in matches:
        try:
            val = float(match.replace(',', '.'))
            if val > 1.0 and val < 100000: 
                found_prices.append(val)
        except:
            continue
            
    if found_prices:
        # En çok tekrar eden en büyük sayı toplam tutar olarak kabul edildi.
        price_counts = Counter(found_prices)
        most_common = price_counts.most_common()
        
        if most_common[0][1] > 1:
            data["total_amount"] = most_common[0][0]
        else:
            data["total_amount"] = max(found_prices)

    return data