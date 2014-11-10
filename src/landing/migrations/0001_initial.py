# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Interesado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(max_length=256)),
                ('modified', models.DateTimeField(default=datetime.datetime(2014, 11, 10, 22, 42, 53, 834857), null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
