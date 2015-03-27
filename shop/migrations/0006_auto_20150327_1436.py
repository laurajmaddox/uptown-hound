# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer_city',
            field=models.CharField(blank=True, max_length=128, verbose_name='City', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='customer_comments',
            field=models.TextField(blank=True, verbose_name='Order comments', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='customer_email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='Email', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='customer_name',
            field=models.CharField(blank=True, max_length=128, verbose_name='Name', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='customer_nation',
            field=django_countries.fields.CountryField(blank=True, max_length=2, verbose_name='Country', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='customer_phone',
            field=models.CharField(blank=True, max_length=32, verbose_name='Phone', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='customer_postal',
            field=models.CharField(blank=True, max_length=64, verbose_name='Zip/Postal Code', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='customer_state',
            field=models.CharField(blank=True, max_length=128, verbose_name='State/Province', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='customer_street',
            field=models.CharField(blank=True, max_length=256, verbose_name='Street Address', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='total_items',
            field=models.DecimalField(blank=True, decimal_places=2, verbose_name='Item Total', null=True, max_digits=6),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='total_order',
            field=models.DecimalField(blank=True, decimal_places=2, verbose_name='Order Total', null=True, max_digits=6),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='total_shipping',
            field=models.DecimalField(blank=True, decimal_places=2, verbose_name='Shipping Total', null=True, max_digits=6),
            preserve_default=True,
        ),
    ]
