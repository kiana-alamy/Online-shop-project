from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .cart import Cart
from .forms import CartAddForm, OfferForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem
# from accounts.models import User
# import datetime
from django.contrib import messages
from shop.models import Product
# from django.conf import settings
# import requests
# import json


class CartView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'orders/cart.html', {'cart': cart})


class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
        return redirect('orders:cart')


class RemoveCardView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('orders:cart')


class OrderDetailView(LoginRequiredMixin, View):
    # form_class = OfferForm

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        # return render(request, 'orders/order.html', {'order': order, 'form': self.form_class})
        return render(request, 'orders/order.html', {'order': order,})


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        # for item in cart:
        #     quant_store = Product.objects.get(slug=item['product'])
        #     if item['quantity'] > quant_store.quantity:
        #         messages.error(
        #             request, f"Sorry, this {item['product']}is not available in the quantity you requested", 'danger')
        #         return redirect('order:cart')
            
        # برای کاربری که لاگین کرده یک سبد خرید ایجاد میشود :
        order = Order.objects.create(user=request.user)
        for item in cart:
            # quant_store = Product.objects.get(slug=item['product'])
            OrderItem.objects.create(
                order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
        #     quant_store.quantity -= item['quantity']
        #     quant_store.save()

        # cart.clear()
        return redirect('orders:order_detail', order.id)




#******************************
# class CheckProfileCart(LoginRequiredMixin, View):
#     def get(self, request):
#         user = Account.objects.get(id=request.user.id)
#         if request.user.postal_code is not None:
#             return render(request, 'orders/checkprofile.html', {'user': user})
#         return render(request, 'orders/error.html')


# class OfferApplyView(LoginRequiredMixin, View):
#     form_class = OfferForm

#     def post(self, request, order_id):
#         now = datetime.datetime.now()
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             code = form.cleaned_data['code']
#             try:
#                 offer = Offer.objects.get(
#                     offer_code__exact=code, start_time__lte=now, expire_time__gte=now, is_available=True)
#             except Offer.DoesNotExist:
#                 messages.error(
#                     request, "This coupon does'nt exist!!!", 'danger')
#                 return redirect('orders:detail_order', order_id)
#             order = Order.objects.get(id=order_id)
#             order.offer = offer.percent
#             order.save()
#             return redirect('orders:detail_order', order_id)


# if settings.SANDBOX:
#     sandbox = 'sandbox'
# else:
#     sandbox = 'www'

# ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
# ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
# ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
# description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# CallbackURL = 'http://127.0.0.1:8080/verify/'


# class OrderPayView(LoginRequiredMixin, View):
#     def get(self, request, order_id):
#         order = Order.objects.get(id=order_id)
#         data = {
#             "MerchantID": settings.MERCHANT,
#             "Amount": order.get_total_price(),
#             "Description": description,
#             "Phone": requests.user.phone_number,
#             "CallbackURL": CallbackURL,
#         }
#         data = json.dumps(data)
#         # set content length by data
#         headers = {'content-type': 'application/json',
#                    'content-length': str(len(data))}
#         try:
#             response = requests.post(
#                 ZP_API_REQUEST, data=data, headers=headers, timeout=10)

#             if response.status_code == 200:
#                 response = response.json()
#                 if response['Status'] == 100:
#                     return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']), 'authority': response['Authority']}
#                 else:
#                     return {'status': False, 'code': str(response['Status'])}
#             return response

#         except requests.exceptions.Timeout:
#             return {'status': False, 'code': 'timeout'}
#         except requests.exceptions.ConnectionError:
#             return {'status': False, 'code': 'connection error'}
