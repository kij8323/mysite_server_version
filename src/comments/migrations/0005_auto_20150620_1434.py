# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0004_auto_20150620_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='reponse',
            field=models.CharField(default=None, max_length=255),
            preserve_default=True,
        ),
    ]
