# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0021_taggeditem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='active',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
