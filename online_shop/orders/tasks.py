from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

print("im hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
@shared_task(bind=True)
def send_order_status_email(self, to_email, message, subject):
    print("im 222222222222222222222222222222222222222222222")
    send_mail(subject , message , 'as.faraso.97@gmail.com' , [to_email])
    print("im 33333333333333333333333333333333333333333333333")
    return f"Email sent to {to_email} successfully"
