from django.urls import path
from . import views

app_name = 'orders'
urlpatterns=[
    path('create/', views.CreateOrderView.as_view() , name='create_order'),
    path('detail/<int:order_id>/' , views.DetailOrderView.as_view(),name='detail_order'),
    path('cart/' , views.CartView.as_view() , name='cart'),
    path('cart/add/<int:product_id>/' , views.CartAddView.as_view() ,name='addcart'),
    path('cart/remove/<int:product_id>/' , views.RemoveCardView.as_view() , name='removecart'),
    # path('checkprofile/' , views.CheckProfileCart.as_view() , name='check'),
    # path('offer/<int:order_id>' ,views.OfferApplyView.as_view() , name='offer'),
    # path('api/', include('orders.api_urls', namespace='api_order')),
    # path('pay/<int:order_id>',views.OrderPayView.as_view(),name='pay'),
]