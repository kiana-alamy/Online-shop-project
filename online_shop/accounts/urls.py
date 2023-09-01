from django.urls import path
from . import views
from .views import ProfileView

app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('verify/', views.UserRegisterVerifyCodeView.as_view(), name='verify_code'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/<int:user_id>/' , ProfileView.as_view() , name='profile'),
]

