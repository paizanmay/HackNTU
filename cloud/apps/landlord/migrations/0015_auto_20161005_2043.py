# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landlord', '0014_landlorduser_bank_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomorderpart',
            name='paid_bank_account',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='roomorderpart',
            name='paid_bank_code',
            field=models.CharField(max_length=3, null=True),
        ),
    ]
