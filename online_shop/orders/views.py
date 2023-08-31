from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .cart import Cart
from shop.models import Product
from accounts.models import User
from .forms import CartAddForm , CouponApplyForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Order, OrderItem, Coupon
import requests
import json
from django.http import HttpResponse
import datetime
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.conf import settings
# from orders.tasks import send_email_fun
from orders.tasks import send_order_status_email


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
    form_class = CouponApplyForm

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'orders/order.html', {'order': order, 'form': self.form_class})


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
		if request.GET.get('Status') == 'OK':
                    user= User.objects.all()
                    cart = Cart(request)
                    cart.clear()
                    to_email = user.email
                    subject = "Order Confirmed Successfuly"
                    message = f"Transaction success order ID: {order_id}"
                    send_order_status_email.delay(to_email ,subject, message)
                    # send_email_fun.delay(subject, message, settings.EMAIL_HOST_USER, to_email)

                    return HttpResponse(f"Transaction success , order ID: {order_id}")
                
		else:
			return HttpResponse('Transaction failed or canceled by user')
                


#******************************
# class CheckProfileCart(LoginRequiredMixin, View):
#     def get(self, request):
#         user = Account.objects.get(id=request.user.id)
#         if request.user.postal_code is not None:
#             return render(request, 'orders/checkprofile.html', {'user': user})
#         return render(request, 'orders/error.html')


class CouponApplyView(LoginRequiredMixin, View):
	form_class = CouponApplyForm

	def post(self, request, order_id):
		now = datetime.datetime.now()
		form = self.form_class(request.POST)
		if form.is_valid():
			code = form.cleaned_data['code']
			try:
				coupon = Coupon.objects.get(code__exact=code, valid_from__lte=now, valid_to__gte=now, active=True)
			except Coupon.DoesNotExist:
				messages.error(request, 'this coupon does not exists', 'danger')
				return redirect('orders:order_detail', order_id)
			order = Order.objects.get(id=order_id)
			order.discount = coupon.discount
			order.save()
		return redirect('orders:order_detail', order_id)