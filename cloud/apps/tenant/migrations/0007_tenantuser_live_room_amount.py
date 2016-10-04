# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0006_auto_20161003_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenantuser',
            name='live_room_amount',
            field=models.IntegerField(default=0),
        ),
    ]
