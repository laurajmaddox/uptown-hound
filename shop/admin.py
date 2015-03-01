from django.contrib import admin
from shop.models import Product, ProdCategory, ProdImage

class ProductAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'slug', 'main_img', 'active', 'category']
    filter_horizontal = ['category']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Product, ProductAdmin)
admin.site.register(ProdCategory)
admin.site.register(ProdImage)