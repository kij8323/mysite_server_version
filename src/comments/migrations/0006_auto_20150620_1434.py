# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0005_auto_20150620_1434'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='reponse',
            new_name='reponsed',
        ),
    ]
