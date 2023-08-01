from django.shortcuts import render
from django.views import View
from shop.models import Product


class HomeView(View):
    # def get(self, request , category_slug=None):
    def get(self, request):
        products = Product.objects.filter(available=True)
        # categories = Category.objects.all()
        # if category_slug:
        #     category = Category.objects.get(slug = category_slug)
        #     products = products.filter(category = category)
        # return render(request, 'index.html', {'products': products , 'categories':categories})
        return render(request, 'base.html', {'products': products ,})