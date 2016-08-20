# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landlord', '0003_auto_20160820_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='deadline_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='notification_date',
            field=models.DateTimeField(null=True),
        ),
    ]
