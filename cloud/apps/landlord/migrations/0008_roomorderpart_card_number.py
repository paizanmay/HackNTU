# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landlord', '0007_roomorderpart_is_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomorderpart',
            name='card_number',
            field=models.CharField(max_length=20L, null=True),
        ),
    ]
