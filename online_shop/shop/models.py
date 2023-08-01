from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from core.models import BaseModel



class Category(models.Model):
    title = models.CharField(max_length=200)
    sub_category = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        related_name='sub_categories', null=True, blank=True
    )
    is_sub = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering= ('title',)
        # برای درست نوشتن مدل جمعه اسم
        verbose_name= 'category' #مفرد
        verbose_name_plural= 'caregories' #جمع

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs): # new
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
        

class Product(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    image = models.ImageField(upload_to='products/%Y/%m/%d')
    title = models.CharField(max_length=250)
    description = models.TextField()
    price = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now= True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('title',)

    def __str__(self) -> str:
        return self.title
        
    def get_absolute_url(self):
        return reverse('shop:details', args=[self.slug])

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     return super().save(*args, **kwargs)