from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Category, Expense
from . services import ExpenseAnalytics # service class'ı
# loglama importu
from logging import getLogger

logger = getLogger(__name__)

class ExpenseAnalyticsTest(TestCase):

    """
    ExpenseAnalytics service katmanının test sınıfı
    """
    def setUp(self):
        """
        Her test çalışmadan önce çalışır ve hazırlık yapar.
        Gerçek veritabanını bozmaz, test bitince buradaki veriler silinir.
        """

    # Test kullanıcı oluşturma
        self.user = User.objects.create_user(username='testuser1', password='testpass123')
        logger.info(f"Test kullanıcısı oluşturuldu: {self.user.username}")

    # Kategori oluşturma
        self.cat_food = Category.objects.create(name='Gıda')
        logger.info(f"Kategori oluşturuldu: {self.cat_food.name}")
        self.cat_transport = Category.objects.create(name='Ulaşım')
        logger.info(f"Kategori oluşturuldu: {self.cat_transport.name}")

    # Harcama ekleme
        Expense.objects.create(user=self.user, amount=800, category=self.cat_food, date='2024-01-15', description='Market alışverişi')
        logger.info(f"Harcama oluşturuldu: 800 TL, Kategori: {self.cat_food.name}")
        Expense.objects.create(user=self.user, amount=150, category=self.cat_transport, date='2024-01-20', description='Otobüs bileti')
        logger.info(f"Harcama oluşturuldu: 150 TL, Kategori: {self.cat_transport.name}")

    def test_calculate_stats(self):
        """
        Service katmanı istatistik hesaplama fonksiyonunun testi
        """
        analytics = ExpenseAnalytics(self.user) # Service class'ından örnek oluşturma
        logger.info("ExpenseAnalytics örneği oluşturuldu.")
        filtered_queryset = analytics.get_filtered_expense({}) # Tüm harcamalar. Boş filtre
        logger.info(f"Filtrelenmiş harcama queryseti alındı: {filtered_queryset.count()} kayıt bulundu.")
        stats = analytics.calculate_stats(filtered_queryset) # İstatistik hesaplama fonksiyonu
        logger.info(f"Harcama istatistikleri hesaplandı: {stats}")

        # Doğrulama aşaması (Assertions)

        # Toplam tutar 950 olmalı (800 + 150)
        self.assertEqual(stats['total_amount'], 950) # Toplam harcama
        logger.info(f"Toplam harcama doğrulandı: {stats['total_amount']}")

        # En yüksek harcama kategorisi 'Gıda' olmalı
        self.assertEqual(stats['most_expensive_category'], 'Gıda') # En yüksek harcama kategorisi
        logger.info(f"En yüksek harcama kategorisi doğrulandı: {stats['most_expensive_category']}")
        
        # Gıda harcaması 800, Ulaşım harcaması 150 olmalı
        self.assertEqual(stats['category_breakdown']['Gıda'], 800)
        self.assertEqual(stats['category_breakdown']['Ulaşım'], 150)
        logger.info(f"Kategori bazlı harcama doğrulandı: {stats['category_breakdown']}")

class ExpenseAPITest(TestCase):
    """
    Expense API uç noktasının test sınıfı. TestCase kullanarak API testi yapar.
    örn: 'APIClient' ile istek gönderme ve yanıt doğrulama, urls yanlış yönlendiriyorsa veya IsAuthenticated izinleri doğru çalıştırıyor mu gibi.
    APIClient kullanarak kod üzerinden sisteme tarayıcı veya postman vs. gibi istek atar.
    """
    def setUp(self):
        # Sanal tarayıcı oluşturma
        self.client = APIClient() # APIClient örneği oluşturma
        logger.info("APIClient örneği oluşturuldu.")

        self.user = User.objects.create_user(username='testuser2', password='testpass456')
        logger.info(f"Test kullanıcısı oluşturuldu: {self.user.username}")
        self.url = '/expenses/stats/' # Test edilecek API uç noktası
        logger.info(f"Test edilecek URL ayarlandı: {self.url}")

    def test_unauthenticated_access(self):
        """
        Senaryo: Giriş yapmamış kullanıcı API'ye erişmeye çalışıyor.
        Beklenen Sonuç: 403 Forbidden
        """
        # Login yapmadan istek atma işlemi
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        logger.info(f"Yetkilendirilmemiş erişim testi yapıldı, durum kodu: {response.status_code}")

    def test_authenticated_access(self):
        """
        Senaryo: Giriş yapmış kullanıcı API'ye erişmeye çalışıyor
        Beklenen Sonuç: 200 OK
        """

        self.client.force_authenticate(user = self.user) # Kullanıcıyı oturum açmış gibi ayarla
        logger.info(f"Kullanıcı oturum açtı: {self.user.username}")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK) # Başarılı erişim doğrulaması (200 OK)
        logger.info(f"Yetkilendirilmiş erişim testi yapıldı, durum kodu: {response.status_code}")