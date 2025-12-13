from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    
    help = 'Otomatik olarak super user oluşturur (Eğer yoksa)'

    def handle(self, *args, **options):
        # Render Environment Variables'dan veya .env'den bilgileri al
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'demo')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'demo@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'demo123')

        if not User.objects.filter(username=username).exists():
            print(f"Kullanici {username} olusturuluyor...")
            User.objects.create_superuser(username, email, password)
            print(f"Superuser '{username}' basariyla olusturuldu!")
        else:
            print(f"Superuser '{username}' zaten var. Atlandi.")
