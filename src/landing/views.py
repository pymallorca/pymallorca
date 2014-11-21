# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
from django.views.generic.base import View
from models import Interesado


def home(request):
    ctx = {}
    return render_to_response('home.html', ctx, RequestContext(request))


def gracias(request):
    ctx = {}
    return render_to_response('gracias.html', ctx, RequestContext(request))


class InteresadoView(View):
    def post(self, request, *args, **kwargs):
        ctx = {}
        email = request.POST.get('email')
        i = Interesado(email=email)
        i.save()
        return render_to_response('gracias.html', ctx, RequestContext(request))