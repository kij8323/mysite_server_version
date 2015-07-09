# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0023_auto_20150427_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='order',
            field=models.PositiveIntegerField(default=1),
            preserve_default=True,
        ),
    ]
