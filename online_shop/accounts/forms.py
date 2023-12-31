# from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from .models import User, OtpCode
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1= forms.CharField(label='password', widget= forms.PasswordInput)
    password2= forms.CharField(label='comfirm password', widget= forms.PasswordInput)
    address2 = forms.CharField(max_length=110)
    postal_code2 = forms.CharField(max_length=11)

    class Meta:
        model= User
        fields= ('email', 'phone_number', 'full_name')

    def clean_password2(self):
        cd= self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('passwords dont match')
        return cd['password2']
    
    def save(self, commit: True):
        user= super().save(commit= False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text='you cant change password using <a href = \'../password/\'></a>')

    class Meta:
        model = User
        fields = ('phone_number', 'full_name', 'last_login',)



class UserRegistrationForm(forms.Form):
    email= forms.EmailField()
    phone_number = forms.CharField(max_length=11)
    full_name = forms.CharField(max_length='200', label='Full name')
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    address2 = forms.CharField(max_length=110)
    postal_code2 = forms.CharField(max_length=11)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] and cd['password2'] and cd['password'] != cd['password2']:
            raise ValidationError('password dont match')
        return cd['password2']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This email already exists')
        return email

    def clean_phone(self):
            phone = self.cleaned_data['phone']
            user = User.objects.filter(phone_number=phone).exists()
            if user:
                raise ValidationError('This phone number already exists')
            OtpCode.objects.filter(phone_number=phone).delete()
            # چک میکنه اگر برای این شماره قبلا کدی بوده اون رو حذف میکنه
            return phone
    
    def address(self):
        return self.cleaned_data['address']
    
    

class VerfiyCodeForm(forms.Form):
    code = forms.IntegerField()


class UserLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11)
    password = forms.CharField(widget=forms.PasswordInput)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('password','last_login','is_admin','is_active','is_superuser','phone_number','groups','user_permissions',)



