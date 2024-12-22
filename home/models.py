
from django.db import models
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return '{}'.format(self.name)

    def get_category_url(self):
        return reverse('category',args=[self.slug])

class Product(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='products')
    description = models.TextField()
    stock = models.IntegerField()
    available = models.BooleanField()
    price = models.IntegerField()
    category_id = models.ForeignKey(Category,on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return '{}'.format(self.name)

    def get_product_url(self):
        return reverse('product_single',args=[self.category_id.slug, self.slug])