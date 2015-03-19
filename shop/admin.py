from django.contrib import admin
from shop.models import Product, ProdCategory, ProdImage, ProdVariation

class ProductAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'slug', 'main_img', 'active', 'category']
    filter_horizontal = ['category']
    prepopulated_fields = {'slug': ('name',)}

class ProdVariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'width', 'price')

admin.site.register(Product, ProductAdmin)
admin.site.register(ProdCategory)
admin.site.register(ProdImage)
admin.site.register(ProdVariation, ProdVariationAdmin)