# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_auto_20150424_0520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='sender_content_type',
            field=models.ForeignKey(related_name='nofity_sender', default=1, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
    ]
