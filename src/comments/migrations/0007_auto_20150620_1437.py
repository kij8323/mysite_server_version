# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0006_auto_20150620_1434'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='reponsed',
        ),
        migrations.AddField(
            model_name='comment',
            name='reponse',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
