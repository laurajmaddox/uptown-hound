from django.contrib import admin
from shop.models import Product, ProdImage

class ProductAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'slug', 'main_img', 'active']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Product, ProductAdmin)
admin.site.register(ProdImage)