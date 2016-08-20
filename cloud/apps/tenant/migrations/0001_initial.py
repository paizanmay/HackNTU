# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import apps.tenant.models


class Migration(migrations.Migration):

    dependencies = [
        ('landlord', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='TenantUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('uuid', models.CharField(default=apps.tenant.models.generate_uuid, max_length=40L)),
                ('username', models.CharField(max_length=100, unique=True, null=True, blank=True)),
                ('fb_id', models.CharField(max_length=100L, unique=True, null=True, db_index=True)),
                ('live_room', models.ForeignKey(related_name='tenant_user', on_delete=django.db.models.deletion.SET_NULL, to='landlord.Room', null=True)),
            ],
            options={
                'db_table': 'tenant_user',
            },
        ),
    ]
