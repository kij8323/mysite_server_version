# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0015_auto_20150620_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='reponse',
            field=models.CharField(default=datetime.datetime(2015, 6, 20, 15, 51, 55, 591938, tzinfo=utc), max_length=255),
            preserve_default=False,
        ),
    ]
