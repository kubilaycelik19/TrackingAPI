# 💰 Smart Expense Tracker API (AI Powered)

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-REST_Framework-092E20?style=for-the-badge&logo=django)
![FastAPI](https://img.shields.io/badge/FastAPI-Microservice-009688?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?style=for-the-badge&logo=postgresql)
![Render](https://img.shields.io/badge/Render-Cloud_Deployment-46E3B7?style=for-the-badge&logo=render)

**Yapay Zeka destekli, Mikroservis mimarisine sahip Akıllı Finans Takip API'si.**

Bu proje, kullanıcının yüklediği fiş/fatura fotoğraflarını **Görüntü İşleme (OCR)** ve **Yapay Zeka** servisleri ile analiz eder. Tarih, işyeri adı ve toplam tutarı otomatik olarak tespit edip veritabanına kaydeder.

---

## 🚀 Canlı Demo (Live Preview)

Proje Render üzerinde canlı yayındadır. Linke tıkladığınızda doğrudan Swagger API Dokümantasyonuna yönlendirilirsiniz.

🔗 **Canlı Sistem:** [https://expense-django-render-linkiniz.onrender.com](https://expense-django-render-linkiniz.onrender.com)
*(Not: Lütfen kendi Render linkinizi buraya yapıştırın)*

> **⚠️ Önemli Not:** Sunucular "Free Tier" (Ücretsiz Plan) olduğu için uyku modunda olabilir. İlk isteğin (Login veya Fiş Yükleme) cevap vermesi **50-60 saniye** sürebilir. Lütfen bekleyiniz.

---

## 🔐 Nasıl Test Edilir? (Adım Adım Yetkilendirme)

Sistem güvenliği **JWT (JSON Web Token)** ile sağlanmaktadır. API'yi test etmek için aşağıdaki adımları izleyin:

### 1. Token Alma (Login)
1.  Swagger arayüzünde **`api`** başlığı altındaki **`/api/token/`** endpoint'ine gidin.
2.  **"Try it out"** butonuna basın.
3.  Aşağıdaki **Demo Kullanıcı** bilgilerini girin ve **Execute** deyin:
    ```json
    {
      "username": "demo",
      "password": "demo123"
    }
    ```
4.  Response body (Yanıt) kısmında gelen **`access`** token değerini (tırnaklar olmadan) kopyalayın.

### 2. Yetkilendirme (Authorize)
1.  Sayfanın sağ üst köşesindeki yeşil **`Authorize`** butonuna tıklayın.
2.  Açılan kutuya token'ı şu formatta yapıştırın:
    
    `Bearer <KOPYALADIGINIZ_TOKEN>`
    
    *(Örnek: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`)*
    **(Dikkat: "Bearer" kelimesi ile token arasında bir boşluk bırakmayı unutmayın!)**

3.  **Authorize** ve ardından **Close** butonuna basın. Artık kilit simgeleri kilitli (🔒) görünecektir.

### 3. Fiş Yükleme ve AI Analizi 🤖
1.  **`expenses`** başlığı altındaki **`/expenses/analyze_receipt/`** endpoint'ini açın.
2.  **"Try it out"** butonuna basın.
3.  **`receipt_image`** alanından bilgisayarınızdaki bir fiş fotoğrafını seçin.
4.  **Execute** butonuna basın.
5.  Sistem fişi işleyecek ve sonucu JSON olarak dönecektir!

---

## 🏗️ Mimari Yapı (Architecture)

Proje, sorumlulukların ayrılması (Separation of Concerns) ilkesine göre **Hibrit Mikroservis** mimarisiyle tasarlanmıştır.

```mermaid
graph LR
    User(Kullanıcı) -- 1. Upload File (Multipart) --> Django[Django Core API]
    Django -- 2. Forward File (Internal Network) --> FastAPI[FastAPI AI Service]
    FastAPI -- 3. Image Processing (OCR) --> Tesseract[Tesseract Engine]
    FastAPI -- 4. Extracted Data (JSON) --> Django
    Django -- 5. Save Expense --> DB[(PostgreSQL)]
