# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0003_tenantuser_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tenantuser',
            name='profile_img_id',
        ),
        migrations.AddField(
            model_name='tenantuser',
            name='profile_img_url',
            field=models.TextField(null=True, blank=True),
        ),
    ]
