from django.contrib.auth.models import User
from django.db import models
from home.models import Product
from urllib3 import request


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,default=None)
    cart_id = models.CharField(max_length=250,unique=True)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.cart_id)

class Items(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)


    def __str__(self):
        return str(self.product)

    def product_total(self):
        return self.product.price * self.quantity


