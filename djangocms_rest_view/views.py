# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.models import Page
from cms.utils.moderator import use_draft
from django.contrib.sites.shortcuts import get_current_site
from menus.menu_pool import menu_pool
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from .serializers import (
    PageSerializer, PageUrlSerializer, PlaceholderListSerializer, PlaceholderSerializer,
    NavigationNodeSerializer
)


class PageViewSet(viewsets.ReadOnlyModelViewSet):

    def get_queryset(self):
        site = get_current_site(self.request)
        if self.action == 'menu':
            return menu_pool.get_nodes(self.request, site_id=site.pk)
        if use_draft(self.request):
            return Page.objects.drafts().on_site(site=site).distinct()
        else:
            return Page.objects.public().on_site(site=site).distinct()

    def get_placeholder(self, obj):
        slot = self.kwargs['placeholder']
        try:
            pk = int(slot)
            return obj.placeholders.get(pk=pk)
        except ValueError:
            return obj.placeholders.get(slot=slot)

    def get_serializer_class(self):
        if self.action == 'placeholders':
            return PlaceholderListSerializer
        elif self.action == 'placeholder':
            return PlaceholderSerializer
        elif self.action == 'menu':
            return NavigationNodeSerializer
        elif self.action == 'urls':
            return PageUrlSerializer
        return PageSerializer

    @list_route()
    def urls(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    @detail_route()
    def placeholders(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    def placeholder(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_placeholder(self.get_object()))
        return Response(serializer.data)

    @list_route()
    def menu(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)
