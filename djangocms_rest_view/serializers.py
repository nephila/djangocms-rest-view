# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from classytags.utils import flatten_context
from cms.models import Page
from django.core.urlresolvers import reverse
from django.utils.translation import get_language_from_request
from rest_framework import serializers
from cms.plugin_rendering import render_placeholder
from rest_framework.serializers import ListSerializer
from sekizai.context import SekizaiContext

from .fields import RecursiveField


class RequestSerializer(object):
    @property
    def request(self):
        return self._context['request']

    @property
    def language(self):
        return get_language_from_request(self.request, check_path=True)


class NavigationNodeSerializer(RequestSerializer, serializers.Serializer):
    title = serializers.CharField(source='get_menu_title', read_only=True)
    url = serializers.SerializerMethodField()
    id = serializers.CharField(read_only=True)
    visible = serializers.BooleanField(read_only=True)
    attributes = serializers.DictField(source='attr', read_only=True)
    children = serializers.ListField(
        child=RecursiveField(), read_only=True
    )
    descendants = serializers.ListField(
        child=RecursiveField(), source='get_descendants', read_only=True
    )
    brothers = serializers.SerializerMethodField()
    path = serializers.SerializerMethodField()

    def get_url(self, obj):
        return reverse('page-detail', args=(obj.id,))

    def get_path(self, obj):
        return obj.get_absolute_url()

    def get_brothers(self, obj):
        brothers = []
        if obj.parent:
            brothers = obj.parent.children
            if brothers:
                brothers = [{'title': node.get_menu_title(), 'id': node.id} for node in brothers if node != obj]
        return brothers


class PlaceholderListSerializer(RequestSerializer, serializers.Serializer):
    placeholders = serializers.SerializerMethodField()

    def get_placeholders(self, obj):
        out = {'sekizai': []}
        for placeholder in obj.placeholders.all():
            serializer = PlaceholderSerializer(placeholder, context=self._context)
            out[placeholder.slot] = serializer.data['content']
            out['sekizai'].append(serializer.data['sekizai'])
        return out


class PlaceholderSerializer(RequestSerializer, serializers.Serializer):

    def to_representation(self, instance):
        context = SekizaiContext()
        context['request'] = self.request
        rendered = render_placeholder(
            instance, context, lang=self.language, editable=False
        ).strip()
        flat = flatten_context(context)
        sekizai_data = {key: list(val) for key, val in flat['SEKIZAI_CONTENT_HOLDER'].items()}
        return {
            'content': rendered,
            'sekizai': sekizai_data
        }


class BasePageSerializer(RequestSerializer, serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    page_title = serializers.SerializerMethodField()
    menu_title = serializers.SerializerMethodField()
    meta_description = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()
    path = serializers.SerializerMethodField()
    template = serializers.SerializerMethodField()
    absolute_url = serializers.SerializerMethodField()
    languages = serializers.ListField(source='get_languages')
    url = serializers.SerializerMethodField()
    redirect = serializers.SerializerMethodField()
    next_page = serializers.SerializerMethodField()
    previous_page = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = [
            'id', 'title', 'placeholders', 'creation_date', 'changed_date', 'publication_date',
            'publication_end_date', 'in_navigation', 'template', 'is_home', 'languages', 'parent',
            'site', 'page_title', 'menu_title', 'meta_description', 'slug', 'url', 'path',
            'absolute_url', 'redirect', 'next_page', 'previous_page'
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

    def get_template(self, obj):
        return obj.get_template()

    def get_absolute_url(self, obj):
        return obj.get_absolute_url(self.language)

    def get_url(self, obj):
        return reverse('page-detail', args=(obj.pk,))

    def get_redirect(self, obj):
        return obj.get_redirect(self.language)

    def get_next_page(self, obj):
        page = obj.get_next_filtered_sibling()
        if page:
            return page.pk

    def get_previous_page(self, obj):
        page = obj.get_previous_filtered_sibling()
        if page:
            return page.pk


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


class PageUrlSerializer(RequestSerializer, serializers.Serializer):
    absolute_url = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    pk = serializers.IntegerField(read_only=True)

    def get_absolute_url(self, obj):
        return obj.get_path()

    def get_url(self, obj):
        return reverse('page-detail', args=(obj.pk,))
