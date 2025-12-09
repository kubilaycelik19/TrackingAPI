from .celery import app as celery_app

# Celery uygulamasını dışa aktarma işlemi.
__all__ = ('celery_app',)