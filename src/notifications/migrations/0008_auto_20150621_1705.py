# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('notifications', '0007_remove_notification_unread'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='reply_content_type',
            field=models.ForeignKey(related_name='reply_object', blank=True, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notification',
            name='reply_object_id',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
