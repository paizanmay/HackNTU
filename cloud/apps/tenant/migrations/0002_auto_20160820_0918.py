# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenantuser',
            name='profile_img_id',
            field=models.CharField(max_length=100L, null=True, db_index=True),
        ),
        migrations.AddField(
            model_name='tenantuser',
            name='sender_id',
            field=models.CharField(max_length=50L, null=True, db_index=True),
        ),
    ]
