from django.urls import path , include
from .views import RegisterView

app_name = 'accounts'
urlpatterns = [
    path('', RegisterView.as_view(), name='register'),
]

