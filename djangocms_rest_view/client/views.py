# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.views.generic import TemplateView


class RestClientView(TemplateView):
    template_name = 'rest/base.html'
