from django.db import models

from shop.constants import ORDER_STATUS_CHOICES


class Order(models.Model):
    """
    Model for a completed customer order
    """
    customer_name = models.CharField(max_length=128, verbose_name='Name', blank=True, null=True)
    customer_street = models.CharField(max_length=256, verbose_name='Street Address', blank=True, null=True)
    customer_city = models.CharField(max_length=128, verbose_name='City', blank=True, null=True)
    customer_state = models.CharField(max_length=128, verbose_name='State/Province', blank=True, null=True)
    customer_nation = models.CharField(max_length=128, verbose_name='Country', blank=True, null=True)
    customer_postal = models.CharField(max_length=64, verbose_name='Zip/Postal Code', blank=True, null=True)
    customer_email = models.EmailField(max_length=254, verbose_name='Email', blank=True, null=True)
    customer_phone = models.CharField(max_length=32, verbose_name='Phone', blank=True, null=True)
    customer_comments = models.TextField(verbose_name='Order comments', blank=True, null=True)

    time = models.DateTimeField(auto_now_add=True, null=True)
    total_items = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Item Total', blank=True, null=True)
    total_shipping = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Shipping Total', blank=True, null=True)
    total_order = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Order Total', blank=True, null=True)
    transaction_id = models.CharField(max_length=128, blank=True, null=True)

    status = models.CharField(max_length=32, choices=ORDER_STATUS_CHOICES, default='Processing')
    shipment_time = models.DateTimeField(blank=True, null=True)
    shipment_method = models.CharField(max_length=128, blank=True, null=True)
    shipment_tracking = models.CharField(max_length=128, blank=True, null=True)


class Product(models.Model):
    """
    Model for products sold in shop
    """
    active = models.BooleanField(default=True)
    category = models.ManyToManyField('ProdCategory')
    description = models.TextField()
    main_img = models.ForeignKey('ProdImage', blank=True, null=True)
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
