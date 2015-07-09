# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0011_auto_20150416_1833'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='video',
            unique_together=set([]),
        ),
    ]
