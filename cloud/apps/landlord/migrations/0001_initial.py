# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apps.landlord.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.CharField(default=apps.landlord.models.generate_uuid, max_length=36L)),
                ('rental', models.IntegerField(null=True)),
                ('name', models.CharField(max_length=100L, null=True, blank=True)),
                ('address', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'landlord_room',
            },
        ),
    ]
