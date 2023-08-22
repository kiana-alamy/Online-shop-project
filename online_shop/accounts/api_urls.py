from django.urls import path
from .api_views import Register
from rest_framework.authtoken import views as token

app_name= 'accounts_api'
urlpatterns = [
    path('register/',Register.as_view() , name='register'),
    path('api-token-auth/' , token.obtain_auth_token),
]