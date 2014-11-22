# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
from django.views.generic import CreateView, TemplateView
from django.core.urlresolvers import reverse_lazy

from models import Interesado
from forms import InteresadoForm


class HomeView(CreateView):
    template_name = 'home.html'
    model = Interesado
    form_class = InteresadoForm
    success_url = reverse_lazy('gracias')


class GraciasView(TemplateView):
    template_name = 'gracias.html'

