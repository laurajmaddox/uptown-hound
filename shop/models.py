# ===============================================
# shop/models.py
# ===============================================

from decimal import Decimal

from django.db import models

from django_countries import Countries
from django_countries.fields import CountryField

from shop.constants import ORDER_STATUS_CHOICES


class Order(models.Model):
    """
    Customer order; created after successful payment
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
    item_total = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name='Item Total',
        default=Decimal('0.00')
    )
    shipping_total = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name='Shipping Total',
        default=Decimal('0.00')
    )
    order_total = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name='Order Total',
        default=Decimal('0.00')
    )
    
    status = models.CharField(max_length=32, choices=ORDER_STATUS_CHOICES, default='Processing')
    shipment_time = models.DateTimeField(blank=True, null=True)
    shipment_method = models.CharField(max_length=128, blank=True, null=True)
    shipment_tracking = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    """
    Size/price variation for a Product in an Order
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
    Product sold in the shop; set active to False for out of stock items
    """
    active = models.BooleanField(default=True)
    category = models.ManyToManyField('ProdCategory')
    description = models.TextField()
    main_img = models.ForeignKey('ProdImage', on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=64)
    related_products = models.ManyToManyField('self', blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.name

    def first_child(self):
        """
        Find leaf in the product category tree path. Assume that next() will
        return a leaf category, but arbitrarily return one of the parent
        categories by default just in case
        """
        child = next(
            (category for category in self.category.all() if not category.is_parent()),
            self.category.all().first()
        )
        return child

    def price_range(self):
        """
        Generate a low to high price range based on ProdVariations for use in templates
        """
        variations = ProdVariation.objects.filter(product=self).order_by('price')
        min_price, max_price = variations.first().price, variations.last().price

        # Return a formatted range when the variations have different prices
        if min_price != max_price:
            return '${:.2f}'.format(min_price) + ' - {:.2f}'.format(max_price)

        # Return the formatted minimum when variations are all the same price
        return '${:.2f}'.format(min_price)

    def thumbnail(self):
        """
        Create a thumbnail of the Product's main image for use in the admin
        """
        return '<img src="%s" width="100" />' % (self.main_img.image.url)

    thumbnail.allow_tags = True


class ProdCategory(models.Model):
    """
    Hierarchical categories for organizing Products
    """
    name = models.CharField(max_length=32)
    parent = models.ForeignKey('self', related_name='children', blank=True, null=True)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = 'product categories'

    def __str__(self):
        return self.name

    def is_parent(self):
        """
        Returns boolean value for whether a category has a child
        """
        return ProdCategory.objects.filter(parent=self).exists()

    def path(self):
        """
        Generates a full URL path for a category that includes all 
        parent categories
        """
        slugs, child = [self.slug], True

        while child:
            if self.parent:
                slugs.append(self.parent.slug)
                self = self.parent
            else:
                # End the loop when the leaf is hit
                child = False

        return '/'.join(slugs[::-1]) + '/'


class ProdImage(models.Model):
    """
    Photo for a Product
    """
    subject = models.ForeignKey('Product')
    tag = models.CharField(max_length=10)
    image = models.FileField(upload_to='products/')

    def __str__(self):
        return self.subject.name + ' ' + self.tag

    def thumbnail(self):
        """
        Creates image thumbnail for use in the admin
        """
        return '<img src="%s" width="100" />' % (self.image.url)
    thumbnail.allow_tags = True


class ProdVariation(models.Model):
    """
    Size/price variation for a Product
    """
    price = models.DecimalField(max_digits=6, decimal_places=2)
    product = models.ForeignKey('Product', related_name='variations', blank=True, null=True)
    size = models.CharField(max_length=64, blank=True, null=True)
    sku = models.CharField(max_length=32, blank=True, null=True)
    sort_order = models.IntegerField(default=0, blank=True, null=True)
    width = models.CharField(max_length=64, blank=True, null=True)
