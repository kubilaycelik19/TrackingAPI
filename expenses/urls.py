from django.urls import path, include
from .views import ExpenseListAPI

urlpatterns = [
    path('', ExpenseListAPI.as_view(), name="expense-list"),
    
]
