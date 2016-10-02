# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landlord', '0011_roomorder_order_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomorder',
            name='deadline',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
