from django.shortcuts import render
from django.views import View
from shop.models import Product , Category
from django.core.paginator import Paginator
from .forms import SearchForm


class HomeView(View):

    def get(self, request , category_slug=None):

        p = Product.objects.all()
        products = Product.objects.all()
        categories = Category.objects.filter( is_sub= False)

        paginator = Paginator(p , 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        products = page_obj

        form = SearchForm()
        if 'search' in request.GET:
            products = Product.objects.all()
            form= SearchForm(request.GET)
            if form.is_valid():
                cd = form.cleaned_data['search']
                products = products.filter(title__icontains = cd)

        if category_slug:
            products = Product.objects.all()
            category = Category.objects.get(slug = category_slug)
            products = products.filter(category = category)
            
        return render(request, 'base.html', {'product': page_obj ,'products': products , 'categories':categories , 'form': form })
    

    # def get(self, request):

    #     p = Product.objects.all()

    #     paginator = Paginator(p , 1)
    #     page_number = request.GET.get('page')
    #     page_obj = paginator.get_page(page_number)

    #     return render(request, 'shop/product.html', {'product': page_obj })



