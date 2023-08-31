from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

print('333333333333333333333333333')

@shared_task(bind=True)
def send_order_status_email(self, to_email, message, subject):
    send_mail(subject , message , settings.EMAIL_HOST_USER , [to_email])
    return f"Email sent to {to_email} successfully"


# @shared_task(serializer='json', name="send_mail")
# def send_email_fun(subject, message, sender, receiver):
#     print('4444444444444444444444444444')
#     send_mail(subject, message, sender, [receiver])