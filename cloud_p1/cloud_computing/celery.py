import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cloud_computing.settings')

cel = Celery('cloud_computing')
cel.config_from_object('django.conf:settings', namespace='CELERY')
cel.autodiscover_tasks()

