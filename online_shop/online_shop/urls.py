from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


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

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   authentication_classes=[],
)

swagger_urls = [
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += swagger_urls
