# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_auto_20150420_2110'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='reponse',
            field=models.TextField(default=None),
            preserve_default=True,
        ),
    ]
