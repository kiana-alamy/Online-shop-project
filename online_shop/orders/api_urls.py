from django.urls import path
from .api_views import OrderApiView


app_name = 'orders_api'

urlpatterns = [
    path('orders_api/', OrderApiView.as_view(), name="order_api"),
]