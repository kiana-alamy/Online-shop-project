from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "online_shop.settings")
app = Celery("online_shop")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.enable_utc = False
app.autodiscover_tasks()
# به صورت خودکار میره تسک هارو پیدا میکنه و اجرا میکنه

# CELERY BEAT SETTINGS
app.conf.beat_schedule = {
    "send-ad-mail-every-week": {
        "task": "products.tasks.send_ad_mails",
        "schedule": crontab(day_of_week="6", hour="16", minute="0"),
    }
}


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))

