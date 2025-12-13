from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from celery.result import AsyncResult

from .models import Expense, Category
from .serializers import ExpenseSerializer, ReceiptAnalysisSerializer
from .services import ExpenseAnalytics
from .tasks import heavy_process_simulation

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    # Kullanıcı sadece kendi verisini görecek.
    def get_queryset(self):
        
        # Eğer bu metod swagger şema oluşturucu tarafından çağrılıyorsa
        if getattr(self, 'swagger_fake_view', False):
            # Boş bir queryset dön, Swagger sadece model yapısına bakar, veriye ihtiyaç duymaz.
            return Expense.objects.none()
            # Gerçek requestte çalışacak.
        return Expense.objects.filter(user=self.request.user)
    
    # Kaydederken kullanıcıyı otomatik ekle.
    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 

    # İstatistik endpoint'i
    # detail=False: Tekbir ID'ye değil, listenin geneline uygulanır.
    @action(detail=False, methods=['get'])
    def stats(self, request): # Harcamaları istatistik fonksiyonlarından geçirip listeleyen fonksiyon
        engine = ExpenseAnalytics(user=request.user)
        expenses = engine.get_filtered_expense(request.query_params)
        stats = engine.calculate_stats(expenses)
        return Response(
            {

            **stats,
            "expenses": ExpenseSerializer(expenses, many=True).data
    })

    # Rapor oluşturma endpoint'i
    @swagger_auto_schema(operation_description="Rapor oluşturma işlemini başlatır ve görev ID'sini döner.")
    @action(detail=False, methods=['post'])
    def report(self, request):
        duration = request.data.get("duration", 10)  # Simülasyon süresi
        task = heavy_process_simulation.delay(duration)
        return Response({
            "message": "Rapor oluşturma talebi alındı.",
            "task_id": task.id,
            "status": "processing"
        }, status=status.HTTP_202_ACCEPTED)
    
    # Görev durumu kontrol endpoint'i
    @action(detail=False, methods=['get'], url_path='check-task/(?P<task_id>[^/.]+)')
    def check_task(self, request, task_id=None):
        task_result = AsyncResult(task_id)
        result = {
            "task_id": task_id,
            "status": task_result.state,
            "result": task_result.result if task_result.ready() else None
        }
        return Response(result)
    
    # Yapay zeka ile fiş analizi endpoint'i
    @swagger_auto_schema(
        method='post',
        request_body=ReceiptAnalysisSerializer,
        responses={201: ExpenseSerializer} # Başarılı olursa oluşturulan objeyi dön
    )
    @action(detail=False, methods=['post'])
    def analyze_receipt(self, request):
        # Veriyi serializer üzerinden alıp doğrulama işlemi.
        serializer = ReceiptAnalysisSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        image_url = serializer.validated_data['image_url']

        # Servis katmanındaki FastAPI Servisi
        engine = ExpenseAnalytics(request.user)
        ai_result = engine.analyze_receipt_via_fastapi(image_url)
        
        # Hata kontrolü
        if "error" in ai_result:
            return Response(ai_result, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        # Otomatik kayıt
        try:
            # Varsayılan kategoriyi bul veya oluştur.
            category, created = Category.objects.get_or_create(name="AI Taraması")

            total_amount = ai_result.get("total_amount", 0)
            merchant = ai_result.get("merchant", "Bilinmiyor")
            date_str = ai_result.get("detected_date", "2025-01-01")

            # Gelen verilerle harcama oluştur
            new_expense = Expense.objects.create(
                user=request.user,
                category=category,
                amount=total_amount,
                description=f"Fiş: {merchant}",
                date=date_str
            )

            return Response(
                ExpenseSerializer(new_expense).data,
                status=status.HTTP_201_CREATED
            )
        
        except Exception as e:
            return Response(
                {"error": f"Otomatik kayıt sırasında hata {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

