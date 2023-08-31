from celery import Celery
from datetime import timedelta
import os
from celery.schedules import crontab



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "online_shop.settings")
app = Celery("online_shop")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.enable_utc = False
app.autodiscover_tasks()
# به صورت خودکار میره تسک هارو پیدا میکنه و اجرا میکنه

# CELERY BEAT SETTINGS
app.conf.beat_schedule = {
    "send_email_every_week": {
        "task": "shop.tasks.send_email_every_week",
        "schedule": crontab(day_of_week="1", hour="12", minute="0"),
    }
}



#***************************help********************************

# celery -A online_shop worker -l info -P solo
# همون پایینه اس اما اسم تسک هارو هم میزاره برامون
# celery -A online_shop worker -l info -P solo --logfile=celery.log
# برای همه ی تسک ها یه دور لاگ میندازه :
# celery -A online_shop beat -l info --logfile=celery.beat.log
