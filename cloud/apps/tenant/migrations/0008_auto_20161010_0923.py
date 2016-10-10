# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0007_tenantuser_live_room_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenantuser',
            name='cust_id',
            field=models.CharField(default='C199063165', max_length=30, blank=True),
        ),
        migrations.AlterField(
            model_name='tenantuser',
            name='bank_account',
            field=models.CharField(default='0000107549900069', max_length=50L, blank=True),
        ),
        migrations.AlterField(
            model_name='tenantuser',
            name='bank_code',
            field=models.CharField(default='822', max_length=3L, blank=True),
        ),
    ]
