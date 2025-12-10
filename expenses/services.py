from django.db.models import Q
from .models import Expense

import requests


class ExpenseAnalytics:

    def __init__(self, user):
        self.user = user

    def get_filtered_expense(self, filters):
        """
        Dictionary (request.query_params) ile filtreleme fonksiyonu.
        args:
            filters: filtreleme kriterleri (category, month, year)
        returns:
            filtrelenmiş Expense queryseti
        """

        queryset = Expense.objects.filter(user=self.user) # Sadece kullanıcının kendi verileri

        if filters.get('category'):
            queryset = queryset.filter(category__name=filters['category'])
        if filters.get('month'):
            queryset = queryset.filter(date__month=filters['month'])
        if filters.get('year'):
            queryset = queryset.filter(date__year=filters['year'])
        return queryset # filtrelenmiş queryseti döndürme işlemi

    def calculate_stats(self, filtered_queryset) -> dict:
        """
        İstatistik hesaplama algortitması.

        args:
            filtered_queryset: filtrelenmiş Expense queryseti

        returns:
            istatistik sözlüğü (dict)
        """

        total_amount = 0
        category_map = {}
        most_expensive = None

        for expense in filtered_queryset:
            total_amount += expense.amount
            category_name = expense.category.name
            if category_name in category_map:
                category_map[category_name] += expense.amount
            else:
                category_map[category_name] = expense.amount
        most_expensive = max(category_map, key=category_map.get) if category_map else None
        return {
            "total_amount": total_amount,
            "most_expensive_category": most_expensive,
            "category_breakdown": category_map
        }

    def analyze_receipt_via_fastapi(self, image_url):
        """
        Django'dan FastAPI servisine istek atar.
        """
        fastapi_url = "http://ai_service:8001/analyze/"

        payload = {"image_url": image_url} # FastAPI'nin beklediği formatta veri

        try:
            # FastAPI'ye POST isteği atma
            response = requests.post(fastapi_url, json=payload, timeout=5)

            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"FastAPI Hatası: {response.status_code}"}
            
        except requests.exceptions.ConnectionError:
            return {"error": "FastAPI servisine ulaşılamadı. Docker konteynerlerini kontrol edin."}

class ExpenseDetail:
    def __init__(self, user):
        self.user = user
