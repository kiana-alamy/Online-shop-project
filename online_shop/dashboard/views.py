from django.shortcuts import render
from django.views import View
from shop.models import Product , Category
from django.core.paginator import Paginator


class HomeView(View):
    def get(self, request , category_slug=None):
        products = Product.objects.filter(available=True)
        categories = Category.objects.filter( is_sub= False)
        paginator = Paginator(products , 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        if category_slug:
            category = Category.objects.get(slug = category_slug)
            products = products.filter(category = category)
        
        return render(request, 'base.html', {'products': page_obj , 'categories':categories})



