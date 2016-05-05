.. highlight:: python

.. module:: cantal_tools


Modules Reference
=================

This is the reference of ``cantal_tools`` package modules.

.. _wsgi metrics:

WSGI metrics
------------

werkzeug_serving
~~~~~~~~~~~~~~~~

.. currentmodule:: cantal_tools.werkzeug_serving

Module provides wrapper around werkzeug's BaseWSGIServer.


.. class:: CantaledWSGIServer

   Wrapper around ``BaseWSGIServer`` from :mod:`werkzeug.serving`

   Usage::

      import cantal
      from cantal_tools import werkzeug_serving

      cantal.start()

      werkzeug_serving.CantaledWSGIServer(
          host='0.0.0.0',
          port=8080,
          ).server_forever()

----

.. _web metrics:

Web metrics
-----------

flask
~~~~~

.. currentmodule:: cantal_tools.flask

Module provides Flask application mixin overriding several methods
for request tracing.

.. class:: FlaskMixin

   Mixin overriding internal application's methods

   :param metrics: Metrics instance

   Usage::

      import flask
      import cantal
      from cantal_tools.flask import FlaskMixin

      class App(FlaskMixin, flask.Flask):
          pass

      cantal.start()

      app = App(__name__)
      app.run()

----

.. _appflow metrics:

Appflow metrics
---------------

redis
~~~~~

.. currentmodule:: cantal_tools.redis

This module provides ``patch_redis`` function and a custom ``Connection`` class:

.. function:: patch_redis(Redis)

   patches ``execute_command`` method of supplied Redis class

   Usage::

      import cantal
      import redis
      from cantal_tools.redis import patch_redis

       cantal.start()

       patch_redis(redis.Redis)
       client = Redis(host='localhost', port=6379)
       client.get('some-key')


If you don't like monkey-patching you can use the following connection class,
however you'd need to instantiate :class:`redis.ConnectionPool` yourself.

.. class:: CantaledConnection

   Wrapper around :class:`redis.Connection`

----

elasticsearch
~~~~~~~~~~~~~

.. currentmodule:: cantal_tools.elasticsearch

.. class:: CantaledTransport

   Wrapper around :class:`elasticsearch.Transport`.
   Overrides ``perform_request`` method.


----

sqlalchemy
~~~~~~~~~~

.. currentmodule:: cantal_tools.sqlalchemy


.. function:: attach_to_engine(engine)

   Attaches listeners to ``before_cursor_execute`` and ``after_cursor_execute``
   engine events.

   :param engine: SQLAlchemy db engine

   Usage::

      import cantal
      import sqlalchemy as sa
      from cantal_tools.sqlalchemy import attach_to_engine

      cantal.start()

      db_engine = sa.create_engine('sqlite:///db.sqlite')
      attach_to_engine(db_engine)

----

django
~~~~~~

.. currentmodule:: cantal_tools.django

.. function:: patch_models_manager(django.db.models.Manager)

   Patches supplied django models :class:`django.db.models.Manager` class
   (wraps ``get_queryset`` method).

   Usage::

      from cantal_tools.django import patch_models_manager
      from django.db import models

      # NOTE: we patch default manager!
      patch_models_manager(models.Manager)
