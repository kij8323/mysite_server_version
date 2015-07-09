# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0007_auto_20150620_1437'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='reponse',
        ),
    ]
