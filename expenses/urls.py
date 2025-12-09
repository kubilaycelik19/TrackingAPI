from django.urls import path, include
from .views import ExpenseListAPI, ExpenseStatsAPI, ExpenseDetailAPI, ExpenseReportAPI, ExpenseTaskStatusAPI

urlpatterns = [
    path('', ExpenseListAPI.as_view(), name="expense-list"),
    path('stats/', ExpenseStatsAPI.as_view(), name="expense-stats"),
    path('<int:id>/', ExpenseDetailAPI.as_view(), name="expense-detail"),
    path('report/', ExpenseReportAPI.as_view(), name="expense-report"),
    path('tasks/<str:task_id>/', ExpenseTaskStatusAPI.as_view(), name="task-status"),
    
]
