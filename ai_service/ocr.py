import pytesseract
from PIL import Image, ImageEnhance, ImageFilter # Görüntü iyileştirme için
import requests
from io import BytesIO
import re
from collections import Counter

def perform_ocr(image_url: str):
    try:
        response = requests.get(image_url, timeout=10)
        image = Image.open(BytesIO(response.content))
        
        # --- GÖRÜNTÜ İYİLEŞTİRME (Pre-processing) ---
        # Resmi siyah-beyaza çevir (Grayscale)
        image = image.convert('L')
        # Kontrast arttırma
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)
        
        # Tesseract Türkçe ayar
        raw_text = pytesseract.image_to_string(image, lang='tur')
        return parse_receipt_text(raw_text)
    except Exception as e:
        print(f"OCR Hatası: {e}")
        return None

def parse_receipt_text(text):
    # Loglama ile ham veriyi görerek hata ayıklama
    print("\n" + "="*30)
    print("HAM METİN:")
    print(text)
    print("="*30 + "\n")

    data = {
        "merchant": "Bilinmiyor",
        "total_amount": 0.0,
        "detected_date": "2025-01-01"
    }
    
    # GÜRÜLTÜ TEMİZLİĞİ
    # Yıldızları ve garip sembolleri temizle
    # Regex
    
    lines = text.split('\n')
    
    # --- İŞYERİ ADI ---
    for line in lines:
        clean = line.strip()
        if len(clean) > 3 and not clean.replace(' ', '').isdigit():
            # Yasaklı kelimeler (Fiş başlıkları vb.)
            if "TEŞEKKÜR" in clean.upper() or "TOPLAM" in clean.upper():
                continue
            data["merchant"] = clean
            break

    # --- TARİH ---
    # DD.MM.YYYY veya DD/MM/YYYY
    date_match = re.search(r'(\d{2}[./]\d{2}[./]\d{4})', text)
    if date_match:
        raw_date = date_match.group(1)
        formatted = raw_date.replace('/', '-').replace('.', '-')
        parts = formatted.split('-')
        if len(parts) == 3:
            data["detected_date"] = f"{parts[2]}-{parts[1]}-{parts[0]}"

    # --- TOPLAM TUTAR---
    # 1. Adım: Tüm sayısal değerleri bul (Regex)
    # Boşlukları silip arayalım: 450, 00 gibi ayrık olmasın
    clean_text_for_price = text.replace(' ', '')
    
    # Regex: En az 1 rakam + (nokta/virgül) + 2 rakam
    matches = re.findall(r'(\d+[.,]\d{2})', clean_text_for_price)
    
    found_prices = []
    for match in matches:
        try:
            # Virgülü noktaya çevir
            val = float(match.replace(',', '.'))
            # Mantıksız tarih gibi sayıları (2024.09 gibi) veya çok küçükleri ele
            if val > 1.0 and val < 100000: 
                found_prices.append(val)
        except:
            continue
            
    if found_prices:
        # En çok tekrar eden en büyük sayıyı bul.
        # Fişte tutar genelde "Toplam", "Kredi Kartı" ve "Matrah" satırlarında tekrar eder.
        # Hatalı okunan genelde 1 kere geçer.
        
        price_counts = Counter(found_prices)
        # En çok tekrar edenleri al
        most_common = price_counts.most_common()
        
        # Eğer tekrar eden bir sayı varsa onu seç
        if most_common[0][1] > 1:
            data["total_amount"] = most_common[0][0]
        else:
            # Hiç tekrar yoksa  en büyüğü al
            # "Tarih mi Tutar mı?" karar vermek için max'ı al
            data["total_amount"] = max(found_prices)

    return data