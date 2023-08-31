from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserSerializer
from rest_framework import status
from .models import OtpCode
from utils import send_otp_code
import random


class UserRegister(APIView):
	def post(self, request):
		ser_data = UserRegisterSerializer(data=request.POST)
		if ser_data.is_valid():
			# ser_data.create(ser_data.validated_data)
			cd = ser_data.validated_data
			rand = random.randint(1000, 9999)
			send_otp_code(cd['phone_number'], rand)
			OtpCode.objects.create(phone_number=cd ['phone_number'], code=rand)
			request.session['user_registration_info'] = {
                'phone_number': cd['phone_number'],
                'firstname': cd['firstname'],
                'lastname': cd['lastname'],
                'password': cd['password']
            }
			return Response(ser_data.data, status=status.HTTP_201_CREATED)
		return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
	