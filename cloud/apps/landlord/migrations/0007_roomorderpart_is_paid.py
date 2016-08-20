# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landlord', '0006_auto_20160820_2024'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomorderpart',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]
