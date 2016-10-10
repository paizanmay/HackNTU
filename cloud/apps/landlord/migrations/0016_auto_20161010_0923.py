# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landlord', '0015_auto_20161005_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='landlorduser',
            name='cust_id',
            field=models.CharField(default='G299287769', max_length=30, blank=True),
        ),
        migrations.AlterField(
            model_name='landlorduser',
            name='bank_account',
            field=models.CharField(default='0000901549904116', max_length=50L, blank=True),
        ),
        migrations.AlterField(
            model_name='landlorduser',
            name='bank_code',
            field=models.CharField(default='822', max_length=3L, blank=True),
        ),
    ]
