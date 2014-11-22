# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from views import *

urlpatterns = patterns('',
    url(r'gracias/$', GraciasView.as_view(), name='gracias'),
    url(r'^$', HomeView.as_view(), name='home'),
)
