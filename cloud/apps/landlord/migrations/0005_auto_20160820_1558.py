# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landlord', '0004_auto_20160820_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='deadline_date',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='notification_date',
            field=models.IntegerField(null=True),
        ),
    ]
