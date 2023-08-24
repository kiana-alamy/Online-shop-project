from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .cart import Cart
from shop.models import Product
from .forms import CartAddForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Order, OrderItem
import requests
import json
from django.http import HttpResponse
import datetime
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.conf import settings
from orders.tasks import send_order_status_email
from accounts import models





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
    

#مونگارد زرین پال 

# MERCHANT = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'
# ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
# ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
# ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
# description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"
# CallbackURL = 'http://127.0.0.1:8000/orders/verify/'

# class OrderPayView(LoginRequiredMixin, View):
# 	def get(self, request, order_id):
# 		# با زدن روی دکمه ی پی سبد خرید خالی میشود :
# 		cart= Cart(request)
# 		cart.clear()
# 		order = Order.objects.get(id=order_id)
#         # آیدی سفارش را در سشن ها ذخیره میکنیم:
# 		request.session['order_pay'] = {
# 			'order_id': order.id,
# 		}		
# 		req_data = {
# 			"merchant_id": MERCHANT,
# 			"amount": order.get_total_price(),
# 			"callback_url": CallbackURL,
# 			"description": description,
# 			# "metadata": {"mobile": request.user.phone_number, "email": request.user.email}
# 		}
# 		req_header = {"accept": "application/json",
# 					  "content-type": "application/json'"}
# 		req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
# 			req_data), headers=req_header)
# 		####################################
# 		authority = req.json()['data']
# 		#####################################
# 		if len(req.json()['errors']) == 0:
# 			return redirect(ZP_API_STARTPAY.format(authority=authority))
# 		else:
# 			e_code = req.json()['errors']['code']
# 			e_message = req.json()['errors']['message']
# 			# return HttpResponse(f"Error code: {e_code}, Error Message: {e_message} رششششششششششششششغ")
# 			return HttpResponse('Transaction failed.\nStatus: ' + str(
# 						req.json()['data']
# 					))
#***********************************************************


if settings.SANDBOX:
    sandbox = "sandbox"
else:
    sandbox = "www"

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = (
    f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
)
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
CallbackURL = "http://127.0.0.1:8000/orders/verify_order/"


class OrderPayView(View):
    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        request.session["order_pay"] = {
            "order_id": order.id,
        }
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": order.get_total_price(),
            "Description": description,
            "CallbackURL": CallbackURL,
            "metadata": {"mobile": order.user.phone_number},
        }
        data = json.dumps(data)
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "content-length": str(len(data)),
        }
        try:
            response = requests.post(
                ZP_API_REQUEST, data=data, headers=headers, timeout=10
            )
            if response.status_code == 200:
                response = response.json()
                if response["Status"] == 100:
                    return redirect(ZP_API_STARTPAY + str(response["Authority"]))
                elif response.get("errors"):
                    e_code = response["errors"]["code"]
                    e_message = response["errors"]["message"]
                    return HttpResponse(
                        f"Error code: {e_code}, Error Message: {e_message}"
                    )
            return HttpResponse(response.items())

        except requests.exceptions.Timeout:
            return {"status": False, "code": "timeout"}
        except requests.exceptions.ConnectionError:
            return {"status": False, "code": "connection error"}


class VerifyOrderView(LoginRequiredMixin, View):
	def get(self, request):
		order_id = request.session['order_pay']['order_id']
		order = Order.objects.get(id=int(order_id))
		t_status = request.GET.get('Status')
		t_authority = request.GET['Authority']
		if request.GET.get('Status') == 'OK':
                    cart = Cart(request)
                    cart.clear()
                    to_email = 'kianaalamy.8182@gmail.com'
                    subject = "Order Confirmed Successfuly"
                    message = f"Transaction success order ID: {order_id}"
                    # print('4444444444444444444444444')
                    send_order_status_email.delay(to_email ,subject, message)

                    return HttpResponse(f"Transaction success , order ID: {order_id}")
                
		else:
			return HttpResponse('Transaction failed or canceled by user')
                


# class VerifyOrderView(View):
#     def get(self, request):

#         order_id = request.session["order_pay"]["order_id"]
#         order = Order.objects.get(id=int(order_id))
#         data = {
#             "MerchantID": settings.MERCHANT,
#             "Amount": order.get_total_price(),
#             "Authority": request.GET["Authority"],
#         }
#         data = json.dumps(data)
#         headers = {
#             "accept": "application/json",
#             "content-type": "application/json",
#             "content-length": str(len(data)),
#         }

#         response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
#         if response.status_code == 200:
#             response = response.json()
#             if response["Status"] == 100 or response["Status"] == 101:
#                 order.status = 2
#                 order.transaction_id = response["RefID"]
#                 order.save()
#                 cart = order.user.cart
#                 # if cart.coupon:
#                 #     coupon = cart.coupon
#                 #     coupon.is_active = False
#                 #     coupon.save()
#                 #     cart.coupon = None
#                 #     cart.save()

#                 for item in cart.cart_items.all():
#                     product = item.product
#                     product.quantity -= item.quantity
#                     if product.quantity == 0:
#                         product.is_active = False
#                     product.save()
#                     item.delete()

#                 # if order.customer.email:
#                 #     mail = order.customer.email
#                 #     message = f"Transaction success.RefID:  {str(response['RefID'])}"
#                 #     mail_subject = "Order Confirmed Successfuly"
#                     # send_order_status_email.delay(mail, message, mail_subject)

#                 return HttpResponse(
#                     f"Transaction success.RefID:  {str(response['RefID'])}, Status: {response['Status']}, order ID: {order_id}"
#                 )
#             else:
#                 order.status = 3
#                 order.save()
#                 return HttpResponse("Transaction failed, order ID:" + str(order_id))
#         return response




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