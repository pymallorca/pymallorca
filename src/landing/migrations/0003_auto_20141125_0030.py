# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0002_auto_20141123_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interesado',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 25, 0, 30, 7, 578895), null=True, blank=True),
        ),
    ]
