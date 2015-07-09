# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='date_of_birth',
        ),
        migrations.AddField(
            model_name='myuser',
            name='first_name',
            field=models.CharField(max_length=120, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='myuser',
            name='is_member',
            field=models.BooleanField(default=False, verbose_name=b'Is Paid Member'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='myuser',
            name='last_name',
            field=models.CharField(max_length=120, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='myuser',
            name='username',
            field=models.CharField(default=datetime.datetime(2015, 4, 17, 21, 8, 31, 266606, tzinfo=utc), unique=True, max_length=255),
            preserve_default=False,
        ),
    ]
