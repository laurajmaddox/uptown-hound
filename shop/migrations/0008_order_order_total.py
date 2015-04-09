# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20150408_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_total',
            field=models.DecimalField(blank=True, null=True, decimal_places=2, verbose_name='Order Total', max_digits=6),
            preserve_default=True,
        ),
    ]
