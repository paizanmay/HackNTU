# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apps.landlord.models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0003_tenantuser_name'),
        ('landlord', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LandlordUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('uuid', models.CharField(default=apps.landlord.models.generate_uuid, max_length=36L)),
                ('username', models.CharField(max_length=100, unique=True, null=True, blank=True)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('bank_account', models.CharField(max_length=100L, null=True, blank=True)),
            ],
            options={
                'db_table': 'landlord_user',
            },
        ),
        migrations.CreateModel(
            name='RoomOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.CharField(default=apps.landlord.models.generate_uuid, max_length=36L)),
                ('amount', models.IntegerField(default=0)),
                ('deadline', models.DateTimeField(null=True)),
                ('room', models.ForeignKey(related_name='room_order', to='landlord.Room')),
            ],
            options={
                'db_table': 'room_order',
            },
        ),
        migrations.CreateModel(
            name='RoomOrderPart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.CharField(default=apps.landlord.models.generate_uuid, max_length=36L)),
                ('amount', models.IntegerField(default=0)),
                ('room', models.ForeignKey(related_name='room_order_part', to='landlord.RoomOrder')),
                ('tenant', models.ForeignKey(related_name='room_order_part', to='tenant.TenantUser')),
            ],
        ),
        migrations.AddField(
            model_name='room',
            name='landlord_user',
            field=models.ForeignKey(related_name='room', to='landlord.LandlordUser', null=True),
        ),
    ]
