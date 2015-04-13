from decimal import Decimal

from django.db import models

from django_countries import Countries
from django_countries.fields import CountryField

from shop.constants import ORDER_STATUS_CHOICES


class Order(models.Model):
    """
    Model for a completed customer order
    """
    customer_name = models.CharField(max_length=128, verbose_name='Name')
    customer_street = models.CharField(max_length=256, verbose_name='Street Address')
    customer_city = models.CharField(max_length=128, verbose_name='City')
    customer_state = models.CharField(max_length=128, verbose_name='State/Province')
    customer_nation = CountryField(verbose_name='Country', blank_label='')
    customer_postal = models.CharField(max_length=64, verbose_name='Zip/Postal Code')
    customer_email = models.EmailField(max_length=254, verbose_name='Email')
    customer_phone = models.CharField(max_length=32, verbose_name='Phone', blank=True, null=True)
    customer_comments = models.TextField(verbose_name='Order comments', blank=True, null=True)

    time = models.DateTimeField(auto_now_add=True, null=True)
    item_total = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Item Total', default=Decimal('0.00'))
    shipping_total = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Shipping Total', default=Decimal('0.00'))
    order_total = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Order Total', default=Decimal('0.00'))

    status = models.CharField(max_length=32, choices=ORDER_STATUS_CHOICES, default='Processing')
    shipment_time = models.DateTimeField(blank=True, null=True)
    shipment_method = models.CharField(max_length=128, blank=True, null=True)
    shipment_tracking = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    """
    Model for a product size/price variation
    """
    order = models.ForeignKey(Order)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    product = models.ForeignKey('Product', blank=True, null=True)
    quantity = models.IntegerField()
    size = models.CharField(max_length=64, blank=True, null=True)
    sku = models.CharField(max_length=32, blank=True, null=True)
    width = models.CharField(max_length=64, blank=True, null=True)


class Product(models.Model):
    """
    Model for products sold in shop
    """
    active = models.BooleanField(default=True)
    category = models.ManyToManyField('ProdCategory')
    description = models.TextField()
    main_img = models.ForeignKey('ProdImage', on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=64)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.name


class ProdCategory(models.Model):
    """
    Model for product organizational tree categories
    """
    name = models.CharField(max_length=32)
    parent = models.ForeignKey('self', related_name='children', blank=True, null=True)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = 'product categories'

    def __str__(self):
        return self.name


class ProdImage(models.Model):
    """
    Model for product images
    """
    subject = models.ForeignKey('Product')
    tag = models.CharField(max_length=10)
    image = models.FileField(upload_to='products/')

    def __str__(self):
        return self.subject.name + ' ' + self.tag


class ProdVariation(models.Model):
    """
    Model for a product size/price variation
    """
    price = models.DecimalField(max_digits=6, decimal_places=2)
    product = models.ForeignKey('Product', related_name='variations', blank=True, null=True)
    size = models.CharField(max_length=64, blank=True, null=True)
    sku = models.CharField(max_length=32, blank=True, null=True)
    width = models.CharField(max_length=64, blank=True, null=True)
