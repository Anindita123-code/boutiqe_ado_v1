from django.contrib import admin
from .models import Products, Category

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )
    ordering = ('sku',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )
    ordering = ('-name',)


admin.site.register(Products, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
