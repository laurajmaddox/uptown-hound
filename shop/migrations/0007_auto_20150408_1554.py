# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20150327_1436'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='total_items',
            new_name='item_total',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='total_shipping',
            new_name='shipping_total',
        ),
        migrations.RemoveField(
            model_name='order',
            name='total_order',
        ),
        migrations.RemoveField(
            model_name='order',
            name='transaction_id',
        ),
        migrations.AlterField(
            model_name='order',
            name='customer_city',
            field=models.CharField(verbose_name='City', default=0, max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='customer_email',
            field=models.EmailField(verbose_name='Email', default=0, max_length=254),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='customer_name',
            field=models.CharField(verbose_name='Name', default=0, max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='customer_nation',
            field=django_countries.fields.CountryField(verbose_name='Country', default=0, max_length=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='customer_postal',
            field=models.CharField(verbose_name='Zip/Postal Code', default=1, max_length=64),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='customer_state',
            field=models.CharField(verbose_name='State/Province', default=0, max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='customer_street',
            field=models.CharField(verbose_name='Street Address', default=0, max_length=256),
            preserve_default=False,
        ),
    ]
