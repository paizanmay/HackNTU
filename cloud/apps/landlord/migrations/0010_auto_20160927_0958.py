# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0003_tenantuser_name'),
        ('landlord', '0009_auto_20160927_0804'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roomorderpart',
            name='name',
        ),
        migrations.AddField(
            model_name='roomorderpart',
            name='replace_pay_user',
            field=models.ForeignKey(to='tenant.TenantUser', null=True),
        ),
    ]
