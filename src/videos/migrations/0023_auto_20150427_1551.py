# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0022_auto_20150427_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
