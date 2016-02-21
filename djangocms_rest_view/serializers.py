# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.models import Page
from django.core.urlresolvers import reverse
from django.utils.translation import get_language_from_request
from rest_framework import serializers
from cms.plugin_rendering import render_placeholder
from rest_framework.serializers import ListSerializer
from sekizai.context import SekizaiContext


class RequestSerializer(object):
    @property
    def request(self):
        return self._context['request']

    @property
    def language(self):
        return get_language_from_request(self.request, check_path=True)


class NavigationNodeSerializer(RequestSerializer, serializers.Serializer):
    title = serializers.CharField(source='get_menu_title', read_only=True)
    ancestors = serializers.ListField(source='get_ancestors', read_only=True)
    descendants = serializers.ListField(source='get_descendants', read_only=True)
    url = serializers.SerializerMethodField()
    id = serializers.CharField(read_only=True)
    visible = serializers.BooleanField(read_only=True)
    attributes = serializers.DictField(source='attr', read_only=True)

    def get_url(self, obj):
        return reverse('page-detail', args=(obj.id,))


class PlaceholderListSerializer(RequestSerializer, serializers.Serializer):
    placeholders = serializers.SerializerMethodField()

    def get_placeholders(self, obj):
        out = {}
        for placeholder in obj.placeholders.all():
            serializer = PlaceholderSerializer(placeholder, context=self._context)
            out[placeholder.slot] = serializer.data['content']
        return out


class PlaceholderSerializer(RequestSerializer, serializers.Serializer):
    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        context = SekizaiContext()
        context['request'] = self.request
        return render_placeholder(
            obj, context, lang=self.language, editable=False
        ).strip()


class BasePageSerializer(RequestSerializer, serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    page_title = serializers.SerializerMethodField()
    menu_title = serializers.SerializerMethodField()
    meta_description = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()
    path = serializers.SerializerMethodField()
    languages = serializers.ListField(source='get_languages')
    url = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = [
            'id', 'title', 'placeholders', 'creation_date', 'changed_date', 'publication_date',
            'publication_end_date', 'in_navigation', 'template', 'is_home', 'languages', 'parent',
            'site', 'page_title', 'menu_title', 'meta_description', 'slug', 'url', 'path'
        ]

    def get_title(self, obj):
        return obj.get_title(self.language)

    def get_page_title(self, obj):
        return obj.get_page_title(self.language)

    def get_menu_title(self, obj):
        return obj.get_menu_title(self.language)

    def get_meta_description(self, obj):
        return obj.get_meta_description(self.language)

    def get_slug(self, obj):
        return obj.get_slug(self.language)

    def get_path(self, obj):
        return obj.get_path(self.language)

    def get_url(self, obj):
        return reverse('page-detail', args=(obj.pk,))

    @classmethod
    def many_init(cls, *args, **kwargs):
        """
        This method implements the creation of a `ListSerializer` parent
        class when `many=True` is used. You can customize it if you need to
        control which keyword arguments are passed to the parent, and
        which are passed to the child.

        Note that we're over-cautious in passing most arguments to both parent
        and child classes in order to try to cover the general case. If you're
        overriding this method you'll probably want something much simpler, eg:

        @classmethod
        def many_init(cls, *args, **kwargs):
            kwargs['child'] = cls()
            return CustomListSerializer(*args, **kwargs)
        """
        kwargs['child'] = BasePageSerializer(*args, **kwargs)
        return ListSerializer(*args, **kwargs)


class PageSerializer(BasePageSerializer):
    placeholders = serializers.SerializerMethodField()

    class Meta(BasePageSerializer.Meta):
        fields = BasePageSerializer.Meta.fields + [
            'placeholders',
        ]

    def get_placeholders(self, obj):
        serializer = PlaceholderListSerializer(obj, context=self._context)
        return serializer.data['placeholders']
