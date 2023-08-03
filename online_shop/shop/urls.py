from django.urls import path , include
from .views import ProductDetailView

app_name='shop'
urlpatterns = [
    path('<slug:slug>/', ProductDetailView.as_view(), name='details'),
]
