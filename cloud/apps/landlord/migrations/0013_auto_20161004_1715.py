# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landlord', '0012_auto_20161002_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomorder',
            name='paid_bank_account',
            field=models.CharField(default='', max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='roomorder',
            name='paid_bank_code',
            field=models.CharField(default='', max_length=3, blank=True),
        ),
    ]
