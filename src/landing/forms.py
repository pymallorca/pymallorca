#!/usr/bin/env python
# encoding: utf-8
# --------------------------------------------------------------------------

from django import forms
from models import Interesado

from captcha.fields import ReCaptchaField


class InteresadoForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Interesado

