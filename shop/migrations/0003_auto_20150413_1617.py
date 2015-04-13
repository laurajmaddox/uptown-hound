# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20150413_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prodvariation',
            name='sort_order',
            field=models.IntegerField(default=0, blank=True, null=True),
            preserve_default=True,
        ),
    ]
