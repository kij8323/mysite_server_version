# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0024_video_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['title', 'timestamp']},
        ),
        migrations.AlterModelOptions(
            name='video',
            options={'ordering': ['order', 'timestamp']},
        ),
    ]
