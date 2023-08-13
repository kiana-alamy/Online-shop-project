from django.shortcuts import render
from django.views import View
from shop.models import Product , Category

class HomeView(View):
    def get(self, request , category_slug=None):
        products = Product.objects.filter(available=True)
        categories = Category.objects.filter( is_sub= False)
        if category_slug:
            category = Category.objects.get(slug = category_slug)
            products = products.filter(category = category)
        return render(request, 'base.html', {'products': products , 'categories':categories})

    # def post(self, request):
    #     return render(request, 'base.html')


