# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import url

from .views import RestClientView

urlpatterns = [
    url(r'^', RestClientView.as_view(), name='rest_client'),
]

