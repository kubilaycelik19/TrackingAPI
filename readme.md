# 💰 Smart Expense Tracker API (AI Powered)

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-REST_Framework-092E20?style=for-the-badge&logo=django)
![FastAPI](https://img.shields.io/badge/FastAPI-Microservice-009688?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?style=for-the-badge&logo=postgresql)
![CI/CD](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?style=for-the-badge&logo=github-actions)

**Yapay Zeka destekli, Mikroservis mimarisine sahip Akıllı Finans Takip API'si.**

Bu proje, kullanıcıların fiş/fatura fotoğraflarını yükleyerek harcamalarını otomatik takip etmelerini sağlar. Kullanıcı bir görsel dosyası yüklediğinde, sistem **Görüntü İşleme (OCR)** ve **Yapay Zeka** servisleri ile analiz yapar; tarih, işyeri adı ve toplam tutarı tespit edip veritabanına kaydeder.

---

## 🚀 Canlı Demo (Live Preview)

Projeyi Render üzerinde canlı olarak test edebilirsiniz. Kayıt olmanıza gerek yoktur, hazır demo kullanıcısı tanımlanmıştır.

🔗 **Canlı Swagger UI:** [https://senin-projen.onrender.com/swagger/](https://senin-projen.onrender.com/swagger/)

### 🔑 Giriş Bilgileri (Demo User)
Sistemi test etmek için sağ üstteki **Authorize** butonuna tıklayın ve aşağıdaki bilgileri girin:

| Key | Value |
| --- | --- |
| **Username** | `demo` |
| **Password** | `demo123` |

*(Not: Sunucu uyku modunda olabilir, ilk isteğin cevap vermesi 30-40 saniye sürebilir.)*

---

## 🏗️ Mimari Yapı (Architecture)

Proje, sorumlulukların ayrılması (Separation of Concerns) ilkesine göre **Hibrit Mikroservis** mimarisiyle tasarlanmıştır.

```mermaid
graph LR
    User(Kullanıcı) -- 1. Upload File (Multipart/Form) --> Django[Django Core API]
    Django -- 2. Forward File (Bytes) --> FastAPI[FastAPI AI Service]
    FastAPI -- 3. Image Processing --> Tesseract[OCR Motoru]
    FastAPI -- 4. Extracted Data (JSON) --> Django
    Django -- 5. Save Expense --> DB[(PostgreSQL)]