# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20150324_2042'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('customer_name', models.CharField(null=True, max_length=128, blank=True)),
                ('customer_street', models.CharField(null=True, max_length=256, blank=True)),
                ('customer_city', models.CharField(null=True, max_length=128, blank=True)),
                ('customer_state', models.CharField(null=True, max_length=128, blank=True)),
                ('customer_nation', models.CharField(null=True, max_length=128, blank=True)),
                ('customer_postal', models.CharField(null=True, max_length=64, blank=True)),
                ('customer_email', models.EmailField(null=True, max_length=254, blank=True)),
                ('customer_phone', models.CharField(null=True, max_length=32, blank=True)),
                ('customer_comments', models.TextField(null=True, blank=True)),
                ('time', models.DateTimeField(null=True, auto_now_add=True)),
                ('total_items', models.DecimalField(null=True, max_digits=6, decimal_places=2, blank=True)),
                ('total_shipping', models.DecimalField(null=True, max_digits=6, decimal_places=2, blank=True)),
                ('total_order', models.DecimalField(null=True, max_digits=6, decimal_places=2, blank=True)),
                ('transaction_id', models.CharField(null=True, max_length=128, blank=True)),
                ('status', models.CharField(choices=[('Processing', 'Processing'), ('Shipped', 'Shipped')], max_length=32, default='Processing')),
                ('shipment_time', models.DateTimeField(null=True, blank=True)),
                ('shipment_method', models.CharField(null=True, max_length=128, blank=True)),
                ('shipment_tracking', models.CharField(null=True, max_length=128, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
