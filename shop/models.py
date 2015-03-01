from django.db import models


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
    parent = models.ForeignKey('self', blank=True, null=True)
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
