from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Expense, Category
from .serializers import ExpenseSerializer, CategorySerializer, ReceiptAnalysisSerializer
from .services import ExpenseAnalytics

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        method='post',
        request_body=ReceiptAnalysisSerializer,
        # Swagger'a dosya yükleme olduğunu söylüyoruz
        consumes=['multipart/form-data'],
        responses={201: ExpenseSerializer}
    )
    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def analyze_receipt(self, request):
        # Veriyi ve Dosyayı Al
        serializer = ReceiptAnalysisSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        # Dosya objesi (InMemoryUploadedFile)
        image_file = serializer.validated_data['receipt_image']
        
        # Servise Gönder
        engine = ExpenseAnalytics(request.user)
        ai_result = engine.analyze_receipt_via_fastapi(image_file)
        
        # Hata Kontrolü
        if "error" in ai_result:
            return Response(ai_result, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            
        # Otomatik Kayıt
        try:
            category, _ = Category.objects.get_or_create(name="AI Taraması")
            
            # FastAPI'den dönen yapı: {"merchant": "...", "total_amount": ...}
            new_expense = Expense.objects.create(
                user=request.user,
                category=category,
                amount=ai_result.get("total_amount", 0),
                description=f"Fiş: {ai_result.get('merchant', 'Bilinmiyor')}",
                date=ai_result.get("detected_date", "2025-01-01")
            )
            
            return Response(
                ExpenseSerializer(new_expense).data, 
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            return Response(
                {"error": f"Otomatik kayıt hatası: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )