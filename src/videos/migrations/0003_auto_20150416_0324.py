# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0002_auto_20150416_0314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='active',
        ),
        migrations.RemoveField(
            model_name='video',
            name='featured',
        ),
        migrations.RemoveField(
            model_name='video',
            name='free_preview',
        ),
    ]
