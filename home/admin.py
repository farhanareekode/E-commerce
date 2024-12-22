
from .models import *

from django.contrib import admin
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields = {'slug':('name',)}
admin.site.register(Category,CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = [ 'name','slug','image','description','stock','available','price','category_id','date']
    prepopulated_fields = {'slug':('name',)}
    list_editable = ['image','description','stock','available','price','category_id','date']
admin.site.register(Product,ProductAdmin)
