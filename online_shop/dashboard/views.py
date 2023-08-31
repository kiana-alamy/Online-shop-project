from django.shortcuts import render
from django.views import View
from shop.models import Product , Category
from django.core.paginator import Paginator
from .forms import SearchForm

class HomeView(View):
    def get(self, request , category_slug=None):
        products = Product.objects.all()
        categories = Category.objects.filter( is_sub= False)

        if category_slug:
            category = Category.objects.get(slug = category_slug)
            products = products.filter(category = category)

        search_form = SearchForm()
        if 'search' in request.GET:
            search_form= SearchForm(request.GET)
            if search_form.is_valid():
                cd = search_form.cleaned_data['search']
                products = products.filter(title__icontains = cd)

        paginator = Paginator(products , 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        products = page_obj
            
        return render(request, 'base.html', {'product': page_obj ,'products': products , 'categories':categories , 'search_form': search_form })