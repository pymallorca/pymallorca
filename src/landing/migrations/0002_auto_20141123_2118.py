# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interesado',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 23, 21, 18, 59, 488616), null=True, blank=True),
        ),
    ]
