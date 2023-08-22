from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category  ,Product
from .serializers import CategorySerializer
from rest_framework import status


class CategoryListView(APIView):
    def get(self, request):
        cat = Category.objects.all()
        ser_data = CategorySerializer(instance=cat, many=True).data
        return Response(ser_data, status=status.HTTP_200_OK)

class ProductListView(APIView):
    def get(self, request):
        pro = Product.objects.all()
        ser_data = CategorySerializer(instance=pro, many=True).data
        return Response(ser_data, status=status.HTTP_200_OK)