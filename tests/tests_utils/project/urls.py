# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include
from django.views.i18n import JavaScriptCatalog
from django.views.static import serve

admin.autodiscover()

urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'^admin/', admin.site.urls),  # NOQA
    url(r'^jsi18n/(?P<packages>\S+?)/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),  # NOQA
    url(r'^api/', include('djangocms_rest_view.urls')),
]

urlpatterns += i18n_patterns(
    url(r'^', include('cms.urls'))  # NOQA
)
