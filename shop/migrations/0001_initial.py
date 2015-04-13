# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django_countries.fields
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('customer_name', models.CharField(verbose_name='Name', max_length=128)),
                ('customer_street', models.CharField(verbose_name='Street Address', max_length=256)),
                ('customer_city', models.CharField(verbose_name='City', max_length=128)),
                ('customer_state', models.CharField(verbose_name='State/Province', max_length=128)),
                ('customer_nation', django_countries.fields.CountryField(verbose_name='Country', max_length=2)),
                ('customer_postal', models.CharField(verbose_name='Zip/Postal Code', max_length=64)),
                ('customer_email', models.EmailField(verbose_name='Email', max_length=254)),
                ('customer_phone', models.CharField(verbose_name='Phone', max_length=32, null=True, blank=True)),
                ('customer_comments', models.TextField(verbose_name='Order comments', blank=True, null=True)),
                ('time', models.DateTimeField(null=True, auto_now_add=True)),
                ('item_total', models.DecimalField(verbose_name='Item Total', max_digits=6, decimal_places=2, default=Decimal('0.00'))),
                ('shipping_total', models.DecimalField(verbose_name='Shipping Total', max_digits=6, decimal_places=2, default=Decimal('0.00'))),
                ('order_total', models.DecimalField(verbose_name='Order Total', max_digits=6, decimal_places=2, default=Decimal('0.00'))),
                ('status', models.CharField(max_length=32, choices=[('Processing', 'Processing'), ('Shipped', 'Shipped')], default='Processing')),
                ('shipment_time', models.DateTimeField(blank=True, null=True)),
                ('shipment_method', models.CharField(max_length=128, blank=True, null=True)),
                ('shipment_tracking', models.CharField(max_length=128, blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('quantity', models.IntegerField()),
                ('size', models.CharField(max_length=64, blank=True, null=True)),
                ('sku', models.CharField(max_length=32, blank=True, null=True)),
                ('width', models.CharField(max_length=64, blank=True, null=True)),
                ('order', models.ForeignKey(to='shop.Order')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProdCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32)),
                ('slug', models.SlugField()),
                ('parent', models.ForeignKey(related_name='children', blank=True, null=True, to='shop.ProdCategory')),
            ],
            options={
                'verbose_name_plural': 'product categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProdImage',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('tag', models.CharField(max_length=10)),
                ('image', models.FileField(upload_to='products/')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=True)),
                ('description', models.TextField()),
                ('name', models.CharField(max_length=64)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('category', models.ManyToManyField(to='shop.ProdCategory')),
                ('main_img', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, null=True, to='shop.ProdImage')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProdVariation',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('size', models.CharField(max_length=64, blank=True, null=True)),
                ('sku', models.CharField(max_length=32, blank=True, null=True)),
                ('sort_order', models.IntegerField(default=0)),
                ('width', models.CharField(max_length=64, blank=True, null=True)),
                ('product', models.ForeignKey(related_name='variations', blank=True, null=True, to='shop.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='prodimage',
            name='subject',
            field=models.ForeignKey(to='shop.Product'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(blank=True, null=True, to='shop.Product'),
            preserve_default=True,
        ),
    ]
