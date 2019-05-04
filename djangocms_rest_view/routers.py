# -*- coding: utf-8 -*-
from rest_framework.routers import DefaultRouter, Route


class CMSRouter(DefaultRouter):
    routes = DefaultRouter.routes + [
        Route(
            url=r'^{prefix}/{lookup}/placeholder/(?P<placeholder>[-\w]+)/$',
            mapping={'get': 'placeholder'},
            name='{basename}-placeholder',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
    ]
