import random
from django.conf import settings
from django.core.exceptions import ValidationError
from kavenegar import KavenegarAPI, APIException, HTTPException
from .models import OtpCode

def verify_code(phone_number, code):
    try:
        otp = OtpCode.objects.get(phone_number=phone_number, code=code)
    except OtpCode.DoesNotExist:
        raise ValidationError('Invalid code')
    else:
        # Remove the OTP from the database after successful verification
        otp.delete()

    # Print the verified OTP code instead of sending it via SMS
    print(f'The OTP code {otp.code} for {otp.phone_number} has been verified successfully')

def send_otp(phone_number):
    # Generate a 6-digit random code
    code = random.randint(100000, 999999)

    # Store the OTP in the database
    otp = OtpCode.objects.create(phone_number=phone_number, code=code)

    print(f'Your verification code is {code}')

    # Send the OTP code via Kavenegar
    # try:
    #     api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
    #     params = {
    #         'sender': 'MYSENDER',
    #         'receptor': phone_number,
    #         'message': f'Your verification code is {code}',
    #     }
    #     api.sms_send(params)
    # except (APIException, HTTPException) as e:
    #     raise ValidationError(str(e))