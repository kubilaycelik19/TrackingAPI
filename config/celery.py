import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings') # Django ayarlarını celery'e belirtme işlemi

# Celery uygulamasını oluşturma
app = Celery(main='config')

# Ayarların 'CELERY' ile başladığını belirtme işlemi
app.config_from_object('django.conf:settings', namespace='CELERY')

# Django app'leri içindeki tasks.py dosyasını otomatik bulma işlemi.
app.autodiscover_tasks()