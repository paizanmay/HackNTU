# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0005_auto_20161003_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenantuser',
            name='bank_account',
            field=models.CharField(default='', max_length=50L, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tenantuser',
            name='bank_code',
            field=models.CharField(default='', max_length=3L, blank=True),
            preserve_default=False,
        ),
    ]
