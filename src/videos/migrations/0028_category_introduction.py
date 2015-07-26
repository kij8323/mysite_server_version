# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0027_category_image_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='introduction',
            field=models.TextField(max_length=5000, null=True, blank=True),
            preserve_default=True,
        ),
    ]
