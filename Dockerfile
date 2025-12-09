# 1. Python'ın hafif bir sürümünü temel al
FROM python:3.10-slim

# 2. Python çıktılarını anında terminale bas (Logları görmek için önemli)
ENV PYTHONUNBUFFERED=1
# .pyc dosyaları oluşturma (Gereksiz yer kaplamasın)
ENV PYTHONDONTWRITEBYTECODE=1

# 3. Konteyner içinde çalışma klasörünü oluştur
WORKDIR /app

# 4. Gereksinim dosyasını kopyala ve yükle
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 5. Projedeki tüm dosyaları konteyner içine kopyala
COPY . /app/

# 6. Konteyner çalıştığında varsayılan olarak bu portu aç (Bilgi amaçlı)
EXPOSE 8000

# 7. (Opsiyonel) Varsayılan komut
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]