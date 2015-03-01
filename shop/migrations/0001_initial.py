# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProdImage',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('description', models.TextField()),
                ('name', models.CharField(max_length=64)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('main_img', models.ForeignKey(blank=True, null=True, to='shop.ProdImage')),
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
    ]
