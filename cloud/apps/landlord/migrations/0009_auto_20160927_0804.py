# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landlord', '0008_roomorderpart_card_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomorder',
            name='name',
            field=models.CharField(default='\u623f\u79df\u8a02\u55ae', max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='roomorderpart',
            name='name',
            field=models.CharField(default='\u623f\u5ba2\u61c9\u4ed8\u623f\u79df', max_length=50, blank=True),
        ),
    ]
