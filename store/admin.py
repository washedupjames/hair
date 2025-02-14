from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'price', 'get_stock_status', 'quantity')
    list_filter = ('quantity',)

    def get_stock_status(self, obj):
        return obj.in_stock  # Return the boolean property directly
    get_stock_status.short_description = 'Stock Status'
    get_stock_status.boolean = True  # Tells Django to display this as a boolean in admin