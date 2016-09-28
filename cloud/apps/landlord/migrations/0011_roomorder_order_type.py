# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landlord', '0010_auto_20160927_0958'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomorder',
            name='order_type',
            field=models.IntegerField(default=0, choices=[(0, b'room'), (1, b'water'), (2, b'electric'), (3, b'internet'), (4, b'other')]),
        ),
    ]
