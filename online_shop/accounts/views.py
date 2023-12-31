from django.shortcuts import render , redirect
from .forms import UserRegistrationForm, VerfiyCodeForm, UserLoginForm, ProfileForm
from django.views import View
import random
from utils import send_otp_code
from .models import OtpCode, User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from orders.models import Order

class ProfileView(View):
    def get(self , request , user_id):
        user = User.objects.get(id = user_id)
        order = Order.objects.filter(user = request.user)
        return render(request , 'accounts/profile.html' , {'user':user ,'order':order})

        

class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            rand = random.randint(1000 , 9999)
            send_otp_code(cd['phone_number'] , rand)
            OtpCode.objects.create(phone_number = cd['phone_number'] , code = rand)
            request.session['user_registration_info'] = {
                'phone_number' : cd['phone_number'] , 
                'full_name': cd['full_name'],
                'password':cd['password'],
                'email': cd['email'],
                'address2': cd['address2'],
                'postal_code2': cd['postal_code2']
            }
        #     # Account.objects.create_user(
        #     #     phone_number=cd['phone_number'], firstname=cd['firstname'], lastname=cd['lastname'], password=cd['password'])
            messages.success(request, 'we sent you a code' , 'success')
            return redirect('accounts:verify_code')
        return render(request , self.template_name,{'form':form})
    


class UserRegisterVerifyCodeView(View):
    form_class = VerfiyCodeForm

    def get(self , request):
        form = self.form_class
        return render(request, 'accounts/verify.html' , {'form':form})
    
    def post(self , request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number = user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if code_instance.code == cd['code']:
                User.objects.create_user(
                email=user_session['email'], phone_number=user_session['phone_number'],
                full_name= user_session['full_name'], password=user_session['password'],
                address2= user_session['address2'], postal_code2= user_session['postal_code2'])
                code_instance.delete()
                messages.success(request , 'you registered baby!!!' , 'success')
                return redirect('home:home')
            else:
                messages.error(request , 'heyyyy! your code is wrong' , 'danger')
                return redirect('register:verify_code')
        return redirect('home:home')
    


class UserLoginView(View):
	form_class = UserLoginForm
	template_name = 'accounts/login.html'

	def get(self, request):
		form = self.form_class
		return render(request, self.template_name, {'form':form})

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(request, phone_number=cd['phone_number'], password=cd['password'])
			if user is not None:
				login(request, user)
				messages.success(request, 'you logged in successfully hiiiiii!!!!', 'info')
				return redirect('home:home')
			messages.error(request, 'phone or password is wrong', 'warning')
		return render(request, self.template_name, {'form':form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'logout successfully byyyy!!!', 'success')
        return redirect('home:home')