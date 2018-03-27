import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('{{cookiecutter.project_name}}')

app.config_from_object('config.settings', namespace='CELERY')
app.autodiscover_tasks()
