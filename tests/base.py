# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from djangocms_helper.base_test import BaseTestCase


class BaseRestView(BaseTestCase):
    _pages_data = (
        {'en': {'title': 'page one', 'template': 'page.html', 'publish': True},
         'fr': {'title': 'page un', 'publish': True},
         'it': {'title': 'pagina uno', 'publish': True}},
        {'en': {'title': 'page two', 'template': 'page.html', 'publish': True},
         'fr': {'title': 'page deux', 'publish': True},
         'it': {'title': 'pagina due', 'publish': True}},
        {'en': {'title': 'page three', 'template': 'page.html', 'publish': True},
         'fr': {'title': 'page trois', 'publish': True},
         'it': {'title': 'pagina tre', 'publish': True}},
    )
