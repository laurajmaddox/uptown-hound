from django.contrib import admin
from shop.models import Order, Product, ProdCategory, ProdImage, ProdVariation


class OrderAdmin(admin.ModelAdmin):
    """
    Order model admin management class
    """
    fieldsets = (
        ('Order Status', { 'fields':
            (
                'status',
                'shipment_time',
                ('shipment_method', 'shipment_tracking')
            )
        }),
        ('Payment', { 'fields': 
            (
                'item_total', 'shipping_total', 'order_total'
            )
        }),
        ('Shipping Info', { 'fields': 
            (
                'customer_name', 'customer_street', 
                ('customer_city', 'customer_state'),
                ('customer_nation', 'customer_postal'), 
                ('customer_email', 'customer_phone'),
                'customer_comments'
            )
        }),
    )
    list_display = ('id', 'customer_name', 'time', 'order_total', 'status')


class ProductAdmin(admin.ModelAdmin):
    """
    Product model admin management class
    """
    fields = ['name', 'description', 'slug', 'main_img', 'active', 'category']
    filter_horizontal = ['category']
    prepopulated_fields = {'slug': ('name',)}


class ProdVariationAdmin(admin.ModelAdmin):
    """
    ProdVariation size/price product variation admin management class
    """
    list_display = ('product', 'size', 'width', 'price', 'sku')


admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProdCategory)
admin.site.register(ProdImage)
admin.site.register(ProdVariation, ProdVariationAdmin)