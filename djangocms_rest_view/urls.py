# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from .routers import CMSRouter
from .views import PageViewSet

router = CMSRouter()
router.register(r'pages', PageViewSet, 'page')
urlpatterns = router.urls
