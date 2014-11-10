# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Interesado


class InteresadosAdmin(admin.ModelAdmin):
    list_display = ('email', 'modified')
    search_fields = ('email', 'modified')
    list_display_links = ('email', 'modified')


admin.site.register(Interesado, admin.ModelAdmin)