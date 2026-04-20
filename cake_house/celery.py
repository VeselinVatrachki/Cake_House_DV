import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cake_house.settings')

app = Celery('cake_house')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()