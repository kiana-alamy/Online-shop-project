from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from accounts.models import Account
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemsSerializer, ItemSerializer
from shop.models import Product, Category


class OrderApiView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        order_ser = OrderSerializer(instance=Order.objects.all(), many=True)
        order_items_ser = OrderItemsSerializer(
        instance=OrderItem.objects.all(), many=True)
        return Response()

    def post(self, request):
        account = Account.objects.get(id=request.user.id) 
        # orderitem = OrderItem.objects.create(user=account)
        self.check_object_permissions(request ,account)
        srz_data = Order(instance = account,data=request.POST, many=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
