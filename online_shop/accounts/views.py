from django.shortcuts import render
from .forms import RegistrationForm
from django.views import View


class RegisterView(View):
    form_class = RegistrationForm
    # print(11111111111111)
    template_name = 'register.html'
    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        # if form.is_valid():
        #     cd = form.cleaned_data
        #     rand = random.randint(1000 , 9999)
        #     send_otp_code(cd['phone_number'] , rand)
        #     OtpCode.objects.create(phone_number = cd['phone_number'] , code = rand)
        #     request.session['user_registration_info'] = {
        #         'phone_number' : cd['phone_number'] , 
        #         'firstname': cd['firstname'],
        #         'lastname':cd['lastname'],
        #         'password':cd['password']
        #     }
        #     # Account.objects.create_user(
        #     #     phone_number=cd['phone_number'], firstname=cd['firstname'], lastname=cd['lastname'], password=cd['password'])
        #     messages.success(request, 'we sent you a code' , 'success')
        #     return redirect('register:verifycode')
        return render(request , 'accounts/register.html',{'form':form})