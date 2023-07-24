from django import forms
from django.core.exceptions import ValidationError



class RegistrationForm(forms.Form):
    phone_number = forms.CharField(max_length=11)
    firstname = forms.CharField(max_length='100', label='First name')
    lastname = forms.CharField(max_length='100', label='Last name')
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] and cd['password2'] and cd['password'] != cd['password2']:
            raise ValidationError('password dont match')
        return cd['password2']