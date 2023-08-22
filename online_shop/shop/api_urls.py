from django.urls import path , include
from .api_views import CategoryListView , ProductListView

app_name ='shop_api'

urlpatterns=[
    path('category/',CategoryListView.as_view() , name='api_category'),
    path('product/',ProductListView.as_view() , name='api_product'),
]