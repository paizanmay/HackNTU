# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landlord', '0013_auto_20161004_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='landlorduser',
            name='bank_code',
            field=models.CharField(max_length=3L, null=True, blank=True),
        ),
    ]
