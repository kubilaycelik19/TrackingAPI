from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, Expense
from . services import ExpenseAnalytics # service class'ı

class ExpenseAnalyticsTest(TestCase):
    def setUp(self):
        """
        Her test çalışmadan önce çalışır ve hazırlık yapar.
        Gerçek veritabanını bozmaz, test bitince buradaki veriler silinir.
        """

    # Test kullanıcı oluşturma
        self.user = User.objects.create_user(username='testuser1', password='testpass123')

    # Kategori oluşturma
        self.cat_food = Category.objects.create(name='Gıda')
        self.cat_transport = Category.objects.create(name='Ulaşım')

    # Harcama ekleme
        Expense.objects.create(user=self.user, amount=800, category=self.cat_food, date='2024-01-15', description='Market alışverişi')
        Expense.objects.create(user=self.user, amount=150, category=self.cat_transport, date='2024-01-20', description='Otobüs bileti')

    def test_calculate_stats(self):
        """
        Service katmanı istatistik hesaplama fonksiyonunun testi
        """
        analytics = ExpenseAnalytics(self.user)
        filtered_queryset = analytics.get_filtered_expense({}) # Tüm harcamalar. Boş filtre
        stats = analytics.calculate_stats(filtered_queryset)

        # Doğrulama aşaması (Assertions)

        # Toplam tutar 950 olmalı (800 + 150)
        self.assertEqual(stats['total_amount'], 950) # Toplam harcama

        # En yüksek harcama kategorisi 'Gıda' olmalı
        self.assertEqual(stats['most_expensive_category'], 'Gıda') # En yüksek harcama kategorisi
        
        # Gıda harcaması 800, Ulaşım harcaması 150 olmalı
        self.assertEqual(stats['category_breakdown']['Gıda'], 800)
        self.assertEqual(stats['category_breakdown']['Ulaşım'], 150)
