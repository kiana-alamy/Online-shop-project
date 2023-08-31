from django.urls import path
from . import api_views
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name= 'accounts_api'
urlpatterns = [
	path('register/', api_views.UserRegister.as_view()),
	path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

router = routers.SimpleRouter()
# router.register('users', api_views.UserViewSet)
urlpatterns += router.urls