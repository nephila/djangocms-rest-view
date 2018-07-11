# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms import api

from djangocms_rest_view.serializers import PageSerializer

from .base import BaseRestView


class TestSerializers(BaseRestView):

    def test_page_serializer(self):
        page_1 = self.get_pages()[0]
        ph = page_1.placeholders.get(slot='content')
        api.add_plugin(ph, 'TextPlugin', language='en', body='test example')
        serializer = PageSerializer(instance=page_1, context={
            'request': self.get_request(page_1, 'en')
        })
        rendered = serializer.data
        self.assertEqual(rendered['slug'], 'page-one')
        self.assertEqual(rendered['placeholders'], {'sekizai': [{}], 'content': 'test example'})
