# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from rest_framework.routers import DefaultRouter, Route


class CMSRouter(DefaultRouter):
    routes = DefaultRouter.routes + [
        Route(
            url=r'^{prefix}/{lookup}/placeholder/(?P<placeholder>[-\w]+)/$',
            mapping={'get': 'placeholder'},
            name='{basename}-placeholder',
            initkwargs={'suffix': 'List'}
        ),
    ]
