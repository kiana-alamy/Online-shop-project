from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from accounts.models import User

print('111111111111111111111111111111')

@shared_task(bind=True)
def send_email_every_week(self):
    mail_subject = "Long time no see!"
    message = "Hi. Visit our site for wonderful new products for your sweet child.\n "

    send_mail(
        subject=mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        fail_silently=False,
    )
    return "TAMMMMMAM"
