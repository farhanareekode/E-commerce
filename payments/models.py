from django.contrib.auth.models import User
from django.db import models
from cart.models import Cart,Items
from home.models import Product


class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address = models.TextField(max_length=200)
    town_city = models.CharField(max_length=160)
    postcode_zip = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField()


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=255)
    ifc_code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    expiry_month = models.CharField(max_length=2)
    expiry_year = models.CharField(max_length=2)
    cvv = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.user.username} - {self.account_number}"


class ProductDetail(models.Model):
    payment = models.ForeignKey('PaymentDone', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Store the price at purchase time
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - Quantity: {self.quantity}"



class PaymentDone(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.order_id} by {self.user.username}"