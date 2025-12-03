from django.urls import path, include
from .views import ExpenseListAPI, ExpenseStatsAPI, ExpenseDetailAPI

urlpatterns = [
    path('', ExpenseListAPI.as_view(), name="expense-list"),
    path('stats/', ExpenseStatsAPI.as_view(), name="expense-stats"),
    path('<int:id>/', ExpenseDetailAPI.as_view(), name="expense-detail"),
    
]
