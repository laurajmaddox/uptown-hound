from django.contrib import admin
from shop.models import Order, OrderItem, Product, ProdCategory, ProdImage, ProdVariation


class OrderItemInline(admin.TabularInline):
    extra = 0
    model = OrderItem
    readonly_fields = ('sku', 'product', 'size', 'width', 'price', 'quantity')


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

    inlines = [OrderItemInline]
    list_display = ('id', 'customer_name', 'time', 'order_total', 'status')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'sku', 'product', 'size', 'width', 'price', 'quantity')
    readonly_fields = ('order', 'product', 'sku', 'size', 'width', 'quantity', 'price')


class ProductAdmin(admin.ModelAdmin):
    """
    Product model admin management class
    """
    readonly_fields = ['thumbnail']
    fields = ['name', 'description', 'slug', 'thumbnail', 'main_img', 'active', 'category']
    filter_horizontal = ['category']
    prepopulated_fields = {'slug': ('name',)}


class ProdCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'path']


class ProdImageAdmin(admin.ModelAdmin):
    readonly_fields = ['thumbnail']
    list_display = ['thumbnail', 'subject']


class ProdVariationAdmin(admin.ModelAdmin):
    """
    ProdVariation size/price product variation admin management class
    """
    fields = ['product', 'size', 'width', 'price', 'sku', 'sort_order']
    list_display = ['product', 'size', 'width', 'price', 'sku']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProdCategory, ProdCategoryAdmin)
admin.site.register(ProdImage, ProdImageAdmin)
admin.site.register(ProdVariation, ProdVariationAdmin)