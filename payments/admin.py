from django.contrib import admin

from .models import Checkout, Payment,PaymentDone,ProductDetail

class CheckoutAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'cart',
        'firstname',
        'lastname',
        'country',
        'address',
        'town_city',
        'postcode_zip',
        'phone',
        'email'
    ]
    search_fields = ['firstname', 'lastname', 'email', 'country', 'town_city']
    list_filter = ['country', 'town_city']
admin.site.register(Checkout, CheckoutAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'account_number',
        'name',
        'expiry_month',
        'expiry_year',
        'cvv',
    ]
    search_fields = ['name', 'account_number', 'user__username']
    list_filter = ['expiry_month', 'expiry_year']

admin.site.register(Payment, PaymentAdmin)


class ProductDetailAdmin(admin.ModelAdmin):
    list_display = ('payment', 'product', 'quantity', 'price','total_price')  # Fields to display in the admin list view
    search_fields = ('product__name', 'payment__order_id')  # Enable search by product name and order ID
    list_filter = ('payment__created_at',)  # Filter by payment creation date
    ordering = ('-payment__created_at',)  # Order by most recent payment

class PaymentDoneAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_id', 'amount', 'created_at')  # Display key fields in the admin interface
    search_fields = ('user__username', 'order_id')  # Enable search by username and order ID
    list_filter = ('created_at',)  # Filter by creation date
    ordering = ('-created_at',)  # Order by most recent payments

# Register models
admin.site.register(ProductDetail, ProductDetailAdmin)
admin.site.register(PaymentDone, PaymentDoneAdmin)
