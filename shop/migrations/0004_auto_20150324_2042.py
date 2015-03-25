# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20150318_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='prodvariation',
            name='sku',
            field=models.CharField(null=True, max_length=32, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='prodvariation',
            name='product',
            field=models.ForeignKey(to='shop.Product', null=True, blank=True, related_name='variations'),
            preserve_default=True,
        ),
    ]
