# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProdCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32)),
                ('slug', models.SlugField()),
                ('parent', models.ForeignKey(blank=True, null=True, to='shop.ProdCategory')),
            ],
            options={
                'verbose_name_plural': 'product categories',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(to='shop.ProdCategory'),
            preserve_default=True,
        ),
    ]
