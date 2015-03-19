# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20150228_2015'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProdVariation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('size', models.CharField(null=True, max_length=64, blank=True)),
                ('width', models.CharField(null=True, max_length=64, blank=True)),
                ('product', models.ForeignKey(null=True, blank=True, to='shop.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='prodcategory',
            name='parent',
            field=models.ForeignKey(null=True, related_name='children', blank=True, to='shop.ProdCategory'),
            preserve_default=True,
        ),
    ]
