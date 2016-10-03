# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0004_auto_20161002_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenantuser',
            name='bank_account',
            field=models.CharField(max_length=50L, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='tenantuser',
            name='bank_code',
            field=models.CharField(max_length=3L, null=True, blank=True),
        ),
    ]
