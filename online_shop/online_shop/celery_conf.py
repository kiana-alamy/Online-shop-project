from celery import Celery
from datetime import timedelta
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_shop.settings')

celery_app = Celery('online_shop')
celery_app.autodiscover_tasks()
# تسک هایی که در پروژه داریم را فراخوانی میکند. در اپ ها هرجا که فایلی به نام تسک داشته باشیم اون فایل رو اجرا میکنه

celery_app.conf.broker_url = 'amqp://'
celery_app.conf.result_backend = 'rpc://'
celery_app.conf.task_serializer = 'json'
celery_app.conf.result_serializer = 'pickle'
celery_app.conf.accept_content = ['json', 'pickle']
celery_app.conf.result_expires = timedelta(days=1)
celery_app.conf.task_always_eager = False
celery_app.conf.worker_prefetch_multiplier = 4