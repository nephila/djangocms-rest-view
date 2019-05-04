# -*- coding: utf-8 -*-
from .routers import CMSRouter
from .views import PageViewSet

router = CMSRouter()
router.register(r'pages', PageViewSet, 'page')
urlpatterns = router.urls
