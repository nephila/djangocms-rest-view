#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from tempfile import mkdtemp

HELPER_SETTINGS = dict(
    INSTALLED_APPS=[
        'rest_framework',
        'djangocms_text_ckeditor',
    ],
    FILE_UPLOAD_TEMP_DIR=mkdtemp(),
    ROOT_URLCONF='tests.test_utils.urls',
)


def run():
    from djangocms_helper import runner
    runner.cms('djangocms_rest_view')


def setup():
    import sys
    from djangocms_helper import runner
    runner.setup('djangocms_rest_view', sys.modules[__name__], use_cms=False)


if __name__ == "__main__":
    run()
