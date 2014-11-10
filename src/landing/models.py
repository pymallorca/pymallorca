# -*- coding: utf-8 -*-

from django.db import models
from datetime import datetime

class Interesado(models.Model):
    email = models.CharField(max_length=256)
    modified = models.DateTimeField(default=datetime.now(), blank=True, null=True)

    def __unicode__(self):
        return self.email