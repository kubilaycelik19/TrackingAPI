from django.test import TestCase
from django.contrib.auth.models import User
from .models import Expense, Category
from rest_framework.test import APIClient
from rest_framework import status

from logging import getLogger
logger = getLogger(__name__)

# ----- Smoke Testi -----

# Temel Django modellerinin ve Viewlarının çalışıp çalışmadığı testi. (CI/CD için)

class ExpenseModelTest(TestCase):
    def setUp(self):
        
        self.user = User.objects.create_user(username='testuser', password="123")
        self.category = Category.objects.create(name="Market")

    def test_create_expense(self):
        # Model seviyesinde kayıt yapılabiliyor mu testi.

        expense = Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=100.50,
            description="Test Harcaması",
            date="2025-01-01"
        )
        self.assertEqual(expense.amount, 100.50) # Amount değerinin 100.50 olup olmadığını sorgular
        self.assertEqual(str(expense), "testuser - Market - 100.5 ₺") # Dönen dict yapısını sorgular.

    class ExpenseAPITest(TestCase):
        def setUp(self):
            self.client = APIClient()
            self.user = User.objects.create_user(username='apiuser', password="123")
            self.client.force_authenticate(user=self.user) # Login olmuş gibi yap
            self.category = Category.objects.create(name='Fatura')

        def test_get_expenses(self):
            # Harcama oluştur
            Expense.objects.create(
                user = self.user,
                category = self.category,
                description = "Api test harcaması",
                amount = 50,
                date = "2025-01-01"
            )

            # Api'den listeyi get ile alma testi
            response =  self.client.get('/expenses/')

            # Response kontrol
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # Listede eleman var mı 
            self.assertEqual(len(response.data), 1)



