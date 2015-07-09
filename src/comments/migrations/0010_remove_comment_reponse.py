# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0009_comment_reponse'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='reponse',
        ),
    ]
