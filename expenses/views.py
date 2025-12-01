from rest_framework.views import APIView  
from rest_framework.response import Response
from rest_framework import status       
from .models import Category, Expense           
from .serializers import ExpenseSerializer

class ExpenseListAPI(APIView):
    """
    /expenses/ endpointi için GET ve POST işlemleri
    """
    def get(self, request):
        print("GET istegi alindi.")
        # veritabanindan tum harcamalar cekildi
        expenses = Expense.objects.all()

        total_amount = 0
        category_map = {} # gıda: 250, ulaştırma: 100 keys: values => key: kategori adı, value: o kategorideki toplam harcama
        for expense in expenses :
            total_amount += expense.amount
            category_name = expense.expense_category.category_name
            if category_name in category_map: 
                category_map[category_name] += expense.amount # varsa: dict[key] += ile sözlük yapısına veri ekleme
            else:
                category_map[category_name] = expense.amount # yoksa: dict[key] = ile sözlük yapısına veri ekleme

        # En çok harcama yapılan kategori

        most_expensive = None
        if category_map:
            most_expensive = max(category_map, key=category_map.get) # sözlükteki en yüksek value'ya sahip key'i döner
        
        return Response({
            "total_expenses": total_amount,
            "most_expensive_category": most_expensive,
            "expenses": ExpenseSerializer(expenses, many=True).data
        })
    
    def post(self, request):
        # Gelen veri serializer'e verildi
        serializer = ExpenseSerializer(data=request.data)
        # Serializer gecerliligi kontrol edildi
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
