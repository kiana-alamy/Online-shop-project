from django.shortcuts import render
from django.views import View
from django.shortcuts import get_object_or_404
from .models import Product
from orders.forms import CartAddForm


class ProductDetailView(View):
    def get(self, request, slug):
        product = Product.objects.get(slug = slug)
        form = CartAddForm()
        return render(request, 'shop/detail.html', {'product': product , 'form': form})
