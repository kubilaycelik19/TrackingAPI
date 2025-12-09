from rest_framework.views import APIView  
from rest_framework.response import Response
from rest_framework import status       
from rest_framework.permissions import IsAuthenticated # Yetki kontrolü
from .models import Category, Expense         
from .services import ExpenseAnalytics  
from .serializers import ExpenseSerializer
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from .tasks import heavy_process_simulation
from celery.result import AsyncResult

class ExpenseListAPI(APIView):

    permission_classes = [IsAuthenticated]  # Sadece yetkili kullanıcılar erişebilir

    def get(self, request):
        """
        /expenses/ endpointi için GET işlemi
        """
        print("GET istegi alindi.")
        # veritabanindan tum harcamalar cekildi

        # Sadece giriş yapan kullanıcının verileri
        expenses = Expense.objects.filter(user=request.user)
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(request_body=ExpenseSerializer)
    def post(self, request):
        """
        /expenses/ endpointi için POST işlemi
        """
        # Gelen veri serializer'e verildi
        serializer = ExpenseSerializer(data=request.data)
        # Serializer gecerliligi kontrol edildi
        if serializer.is_valid():
            # Kaydederken user bilgisi ekleme işlemi
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
class ExpenseStatsAPI(APIView):
    """
    /expenses/stats/ endpointi için GET işlemi (Filtereleme ve istatistik)
    """

    permission_classes = [IsAuthenticated]  # Sadece yetkili kullanıcılar erişebilir

    def get(self, request):
        
        engine = ExpenseAnalytics(user=request.user) # Class ile nesne oluşturma işlemi
        filtered_expenses = engine.get_filtered_expense(request.query_params) # Filtreleme işlemi
        stats = engine.calculate_stats(filtered_expenses) # İstatistik hesaplama işlemi
        
        return Response({
            **stats, # Dictionary unpacking işlemi. (Sözlüğü açıp dökme işlemi.)

            # Stats sözlüğü ve serialized data'yı birleştirip değer döndürme işlemi.
            "expenses": ExpenseSerializer(filtered_expenses, many=True).data 
        })

class ExpenseDetailAPI(APIView):
    
    permission_classes = [IsAuthenticated] # Sadece yetkili kullanıcılar erişebilir

    def get_object(self, id, user):

        obj = get_object_or_404(Expense, id=id, user=user)
        return obj
    
    def get(self, request, id):
        """
        /expenses/<id>/ endpointi ile detail GET işlemi
        """
        expense = self.get_object(id, request.user)
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)
    
    @swagger_auto_schema(request_body=ExpenseSerializer)
    def put(self, request, id):
        """
        /expenses/<id>/ endpointi için PUT işlemi
        """
        
        expense = self.get_object(id, request.user)
        serializer = ExpenseSerializer(instance=expense, data=request.data)
        # Güncelleme işleminde 'instance' parametresi verilir.

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        """
        /expenses/<id>/ endpointi için DELETE işlemi
        """
        expense = self.get_object(id, request.user)
        expense.delete()
        return Response({"Message": "Harcama başarıyla silindi!"}, status=status.HTTP_204_NO_CONTENT)

class ExpenseReportAPI(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        duration = request.data.get('duration', 10) # Varsayılan olarak son 10
        tasks = heavy_process_simulation.delay(duration=duration)

        return Response({
            "message": "Rapor oluşturma talebi alındı. Arka planda işleniyor.",
            "task_id": tasks.id, # Task ID'si. Bununla durum sorgulanabilir.
            "status:": tasks.status,
        }, status=status.HTTP_202_ACCEPTED)
    
class ExpenseTaskStatusAPI(APIView):

    def get(self, request, task_id):
        task_result = AsyncResult(id=task_id)

        result = {
            "task_id": task_id,
            "status": task_result.status,
            "result": task_result.result if task_result.ready() else None # Eğer görev tamamlandıysa sonucu döndür.
        }
        return Response(result)
    