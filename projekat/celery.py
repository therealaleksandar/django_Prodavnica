import os
from celery import Celery

# postavi default Django podesavanja modul za celery program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projekat.settings')

app = Celery('prodavnica')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
