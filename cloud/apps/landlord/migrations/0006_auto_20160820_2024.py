# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landlord', '0005_auto_20160820_1558'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roomorderpart',
            old_name='room',
            new_name='room_order',
        ),
    ]
