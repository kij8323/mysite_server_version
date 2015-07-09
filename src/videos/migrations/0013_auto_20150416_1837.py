# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0012_auto_20150416_1836'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='slug',
        ),
        migrations.AlterField(
            model_name='video',
            name='category',
            field=models.ForeignKey(to='videos.Category', null=True),
            preserve_default=True,
        ),
    ]
