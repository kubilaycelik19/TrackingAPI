from rest_framework.views import APIView  
from rest_framework.response import Response
from rest_framework import status       
from rest_framework.permissions import IsAuthenticated # Yetki kontrolü
from .models import Category, Expense         
from .services import ExpenseAnalytics  
from .serializers import ExpenseSerializer
from django.shortcuts import get_object_or_404

class ExpenseListAPI(APIView):
    """
    /expenses/ endpointi için GET ve POST işlemleri
    """

    permission_classes = [IsAuthenticated]  # Sadece yetkili kullanıcılar erişebilir

    def get(self, request):
        print("GET istegi alindi.")
        # veritabanindan tum harcamalar cekildi

        # Sadece giriş yapan kullanıcının verileri
        expenses = Expense.objects.filter(user=request.user)
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)
    
    def post(self, request):
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
    """
    /expenses/delete/<id>/ endpointi için DELETE işlemi
    
    """
    permission_classes = [IsAuthenticated] # Sadece yetkili kullanıcılar erişebilir

    def get_object(self, id, user):

        obj = get_object_or_404(Expense, id=id, user=user)
        return obj
    
    def get(self, request, id):
        
        expense = self.get_object(id, request.user)
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)
    
    def put(self, request, id):
        
        expense = self.get_object(id, request.user)
        serializer = ExpenseSerializer(instance=expense, data=request.data)
        # Güncelleme işleminde 'instance' parametresi verilir.

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        expense = self.get_object(id, request.user)
        expense.delete()
        return Response({"Message": "Harcama başarıyla silindi!"}, status=status.HTTP_204_NO_CONTENT)

