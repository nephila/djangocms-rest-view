===================
djangocms-rest-view
===================

.. image:: https://img.shields.io/pypi/v/djangocms-rest-view.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-rest-view
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/djangocms-rest-view.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-rest-view
    :alt: Monthly downloads

.. image:: https://img.shields.io/pypi/pyversions/djangocms-rest-view.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-rest-view
    :alt: Python versions

.. image:: https://img.shields.io/travis/nephila/djangocms-rest-view.svg?style=flat-square
    :target: https://travis-ci.org/nephila/djangocms-rest-view
    :alt: Latest Travis CI build status

.. image:: https://img.shields.io/coveralls/nephila/djangocms-rest-view/master.svg?style=flat-square
    :target: https://coveralls.io/r/nephila/djangocms-rest-view?branch=master
    :alt: Test coverage

.. image:: https://img.shields.io/codecov/c/github/nephila/djangocms-rest-view/develop.svg?style=flat-square
    :target: https://codecov.io/github/nephila/djangocms-rest-view
    :alt: Test coverage

.. image:: https://codeclimate.com/github/nephila/djangocms-rest-view/badges/gpa.svg?style=flat-square
   :target: https://codeclimate.com/github/nephila/djangocms-rest-view
   :alt: Code Climate

An application to load django CMS pages in a client application.

djangocms-rest-view uses Django REST framework to serve django CMS pages through a REST API

Editing must still be done the "traditional" way

Installation
------------

* pip install djangocms-rest-view
* Edit ``INSTALLED_APPS``::

    INSTALLED_APPS = [
        ...
        'rest_framework',
        'djangocms_rest_view',
        ...
    ]

* Edit ``urls.py``::

    urlpatterns = [
        ...
        url(r'^api/', include('djangocms_rest_view.urls')),
        ...
    ]

* That's all!

The REST view of the pages will be available at http://example.com/api/

Sample client
-------------

A sample Angular JS client is provided within the project.

To start exploring djangocms-rest view, you can install it and browse the website:

* Edit ``INSTALLED_APPS``::

    INSTALLED_APPS = [
        ...
        'djangocms_rest_view.client',
        ...
    ]

* Edit ``urls.py``::

    urlpatterns = [
        ...
        url(r'^rest/', include('djangocms_rest_view.client.urls')),
        ...
    ]

the Angular client will be available at http://example.com/rest/

* Install dependencies according to the application bower.json: https://gitix.iast.it/opensource/djangocms-rest-view/blob/master/bower.json

example:

* Copy dependencies in project ``bower.json``
* run bower::

    bower install

Customize
---------

The sample client uses a dedicated base page to load all the default styles etc needed to render
your content.
Template is in ``rest/base.html`` copy it from ``djangocms_rest_view/client/templates/rest/base.html``
and edit it according your needs.

Features
--------

* REST view to the pages
* Support for sekizai context in the plugins

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  cookiecutter-djangopackage-helper_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _cookiecutter-djangopackage-helper: https://github.com/nephila/cookiecutter-djangopackage-helper
