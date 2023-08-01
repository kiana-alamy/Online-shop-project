# from django.shortcuts import render
# from django.views import View
# from django.shortcuts import get_object_or_404
# from .models import Product
# from order.forms import CartAddForm


# class ProductDetailView(View):
#     def get(self, request, slug):
#         product = Product.objects.get(slug = slug)
#         # comment = Comment.objects.filter(product_id = product.id)
#         form = CartAddForm()
#         return render(request, 'product/detail.html', {'product': product , 'form':form , 'comment':comment})
