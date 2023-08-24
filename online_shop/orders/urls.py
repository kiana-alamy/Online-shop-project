from django.urls import path
from . import views

app_name = 'orders'
urlpatterns=[
    path('create/', views.OrderCreateView.as_view() , name='order_create'),
    path('detail/<int:order_id>/' , views.OrderDetailView.as_view(),name='order_detail'),
    path('cart/' , views.CartView.as_view() , name='cart'),
    path('cart/add/<int:product_id>/' , views.CartAddView.as_view() ,name='addcart'),
    path('cart/remove/<int:product_id>/' , views.RemoveCardView.as_view() , name='cart_remove'),
    # path('checkprofile/' , views.CheckProfileCart.as_view() , name='check'),
    path('apply/<int:order_id>' ,views.CouponApplyView.as_view() , name='apply_coupon'),
    # path('api/', include('orders.api_urls', namespace='api_order')),
    path('pay/<int:order_id>',views.OrderPayView.as_view(),name='order_pay'),
    path('verify_order/', views.VerifyOrderView.as_view(), name='order_verify'),
]