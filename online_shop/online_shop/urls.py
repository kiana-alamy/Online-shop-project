from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace= 'accounts')),
    path('shop/', include('shop.urls', namespace= 'shop')),
    path('', include('dashboard.urls', namespace= 'home')),
    path('orders/' , include('orders.urls', namespace='orders')),
    path('api-auth/', include('rest_framework.urls'))
]+ static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT) #برای نشون دادن عکس ها در برنامه

