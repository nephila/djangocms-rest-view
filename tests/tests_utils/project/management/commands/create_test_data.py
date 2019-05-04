# -*- coding: utf-8 -*-
from random import randrange, randint

from cms import api
from django.core.management import BaseCommand
from django.utils.lorem_ipsum import words
from djangocms_helper.base_test import BaseTestCaseMixin


class Command(BaseCommand):
    help = 'Create pages.'

    def handle(self, *args, **options):
        _pages_data = (
            {'en': {'title': 'page one', 'template': 'page.html', 'publish': True}},
            {'en': {'title': 'page two', 'template': 'page.html', 'publish': True, 'parent': 'page-one'}},
            {'en': {'title': 'page three', 'template': 'page.html', 'publish': True, 'parent': 'page-one'}},
            {'en': {'title': 'page four', 'template': 'page.html', 'publish': True, 'parent': 'page-three'}},
            {'en': {'title': 'page five', 'template': 'page.html', 'publish': True, 'parent': 'page-three'}},
            {'en': {'title': 'page six', 'template': 'page.html', 'publish': True, 'parent': 'page-five'}},
            {'en': {'title': 'page seven', 'template': 'page.html', 'publish': True, 'parent': 'page-five'}},
            {'en': {'title': 'page eight', 'template': 'page.html', 'publish': True, 'parent': 'page-two'}},
            {'en': {'title': 'page nine', 'template': 'page.html', 'publish': True, 'parent': 'page-eight'}},
            {'en': {'title': 'page ten', 'template': 'page.html', 'publish': True, 'parent': 'page-nine'}},
            {'en': {'title': 'page eleven', 'template': 'page.html', 'publish': True, 'parent': 'page-eight'}},
            {'en': {'title': 'page twelve', 'template': 'page.html', 'publish': True, 'parent': 'page-eleven'}},
        )
        pages = BaseTestCaseMixin.create_pages(_pages_data, ['en'])
        for page in pages:
            for x in range(0, randint(4, 8)):
                api.add_plugin(
                    placeholder=page.get_placeholders().get(slot='content'), plugin_type='TextPlugin',
                    body=words(count=10), language='en'
                )
            page.publish('en')
