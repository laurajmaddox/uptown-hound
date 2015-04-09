# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_order_order_total'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('prodvariation_ptr', models.OneToOneField(to='shop.ProdVariation', parent_link=True, auto_created=True, primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('order', models.ForeignKey(to='shop.Order')),
            ],
            options={
            },
            bases=('shop.prodvariation',),
        ),
    ]
