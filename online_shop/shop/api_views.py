from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category  ,Product
from .serializers import CategorySerializer
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
# کش

class CategoryListView(APIView):
    def get(self, request):
        cat = Category.objects.all()
        ser_data = CategorySerializer(instance=cat, many=True).data
        return Response(ser_data, status=status.HTTP_200_OK)

# تایمش میشه بیشتر هم باشه
class ProductListView(APIView):
    @method_decorator(cache_page(180))
    def get(self, request):
        pro = Product.objects.all()
        ser_data = CategorySerializer(instance=pro, many=True).data
        return Response(ser_data, status=status.HTTP_200_OK)