# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('landlord', '0002_auto_20160820_1348'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='landlorduser',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterModelTable(
            name='roomorderpart',
            table='room_order_part',
        ),
    ]
