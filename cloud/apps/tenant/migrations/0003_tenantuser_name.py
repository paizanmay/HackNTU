# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0002_auto_20160820_0918'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenantuser',
            name='name',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
