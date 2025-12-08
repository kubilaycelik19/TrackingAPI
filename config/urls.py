from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Akıllı Harcama Takip API",
      default_version='v1',
      description="Bu API kullanıcıların harcamalarını takip etmesini ve istatistik almasını sağlar.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@expenses.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('expenses/', include('expenses.urls')),

    # Dökümantasyon URL'leri
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
