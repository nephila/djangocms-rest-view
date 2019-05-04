#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tempfile import mkdtemp

HELPER_SETTINGS = dict(
    INSTALLED_APPS=[
        'djangocms_text_ckeditor',
        'rest_framework',
        'tests.tests_utils.project',
    ],
    FILE_UPLOAD_TEMP_DIR=mkdtemp(),
    ROOT_URLCONF='tests.tests_utils.project.urls'
)


def run():
    from djangocms_helper import runner
    runner.cms('djangocms_rest_view')


def setup():
    import sys
    from djangocms_helper import runner
    runner.setup('djangocms_rest_view', sys.modules[__name__], use_cms=True)


if __name__ == "__main__":
    run()
