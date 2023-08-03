# from django.db import models
# from django.contrib.auth import get_user_model
# from shop.models import Product
# from django.core.validators import MinValueValidator, MaxValueValidator


# class Order(models.Model):
# 	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='order_s')
# 	paid = models.BooleanField(default=False)
# 	created = models.DateTimeField(auto_now_add=True)
# 	updated = models.DateTimeField(auto_now=True)
# 	discount = models.IntegerField(blank=True, null=True, default=None)

# 	class Meta:
# 		ordering = ('paid', '-updated')

# 	def __str__(self):
# 		return f'{self.user} - {str(self.id)}'

# 	def get_total_price(self):
# 		total = sum(item.get_cost() for item in self.items.all())
# 		if self.discount:
# 			discount_price = (self.discount / 100) * total
# 			return int(total - discount_price)
# 		return total
	

# class OrderItem(models.Model):
# 	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='item_s')
# 	product = models.ForeignKey(Product, on_delete=models.CASCADE)
# 	price = models.IntegerField()
# 	quantity = models.IntegerField(default=1)

# 	def __str__(self):
# 		return str(self.id)

# 	def get_cost(self):
# 		return self.price * self.quantity


from django.db import models
from core.models import BaseModel
from shop.models import Product
from accounts.models import User
from django.core.validators import MinValueValidator , MaxValueValidator

class Order(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders')
    state = models.CharField(max_length=100, null=True)
    paid = models.BooleanField(default=False)
    description = models.CharField(max_length=100, null=True)
    created = models.DateTimeField(auto_now_add=True)
    offer = models.IntegerField(default=None , null=True , blank=True)
    discount = models.IntegerField(default=None , null=True , blank=True)
    def __str__(self) -> str:
        return f'{self.user}'

    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.offer:
            discount_price = (self.offer /100)*total
            return (total - discount_price)
        return total


class OrderItem(BaseModel):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f'{self.quantity}'

    def get_cost(self):
        return self.price*self.quantity


# class Offer(BaseModel):
#     expire_time = models.DateTimeField()
#     start_time = models.DateTimeField()
#     percent = models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(90)])
#     offer_code = models.CharField(max_length=100, unique=True)
#     is_available = models.BooleanField(default=False)

#     def __str__(self) -> str:
#         return self.offer_code
