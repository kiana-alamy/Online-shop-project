from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializers, VerifySerializers, ProfileSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Account, OtpCode
# from .permissions import IsOwnerOrReadOnly
from utils import send_otp_code
import random


class Register(APIView):
    def post(self, request):
        ser_data = RegisterSerializers(data=request.POST)
        if ser_data.is_valid():
            cd = ser_data.validated_data
            rand = random.randint(1000, 9999)
            send_otp_code(cd['phone_number'], rand)
            OtpCode.objects.create(phone_number=cd['phone_number'], code=rand)
            request.session['user_registration_info'] = {
                'phone_number': cd['phone_number'],
                'firstname': cd['firstname'],
                'lastname': cd['lastname'],
                'password': cd['password']
            }
            # ser_data.create(ser_data.validated_data)
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeView(APIView):
    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(
            phone_number=user_session['phone_number'])
        ser_data = VerifySerializers(data=request.POST)
        if ser_data.is_valid():
            cd = ser_data.validated_data
            if code_instance.code == cd['code']:
                Account.objects.create_user(
                    phone_number=user_session['phone_number'], firstname=user_session['firstname'], lastname=user_session['lastname'], password=user_session['password'])
                code_instance.delete()
                return Response(ser_data.data, status=status.HTTP_201_CREATED)
            return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)