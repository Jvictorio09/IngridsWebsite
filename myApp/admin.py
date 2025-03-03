from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_on_sale', 'sale_price')
    list_filter = ('is_on_sale',)
    search_fields = ('name', 'description')
