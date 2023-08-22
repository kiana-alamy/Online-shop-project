from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace= 'accounts')),
    path('accounts_api/', include('accounts.api_urls', namespace= 'accounts_api')),
    path('shop/', include('shop.urls', namespace= 'shop')),
    path('shop_api/', include('shop.api_urls', namespace= 'shop_api')),
    path('', include('dashboard.urls', namespace= 'home')),
    path('orders/' , include('orders.urls', namespace='orders')),
    path('orders_api/' , include('orders.api_urls', namespace='orders_api')),
    path('api-auth/', include('rest_framework.urls'))
]+ static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT) #برای نشون دادن عکس ها در برنامه

