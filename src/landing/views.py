# -*- coding: utf-8 -*-

from django.views.generic import CreateView, TemplateView
from django.core.urlresolvers import reverse_lazy

from models import Interesado
from forms import InteresadoForm
import random


class HomeView(CreateView):
    template_name = 'home.html'
    model = Interesado
    form_class = InteresadoForm
    success_url = reverse_lazy('gracias')

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['number'] = Interesado.objects.count()
        return context

class GraciasView(TemplateView):
    template_name = 'gracias.html'

