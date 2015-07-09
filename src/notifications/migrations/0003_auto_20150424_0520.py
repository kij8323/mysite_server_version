# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_auto_20150424_0514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='sender_content_type',
            field=models.ForeignKey(related_name='nofity_sender', blank=True, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
    ]
