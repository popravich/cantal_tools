.. highlight:: python

.. module:: cantal_tools


Modules Reference
=================

This is the reference of ``cantal_tools`` package modules.

WSGI metrics
------------

werkzeug
~~~~~~~~

.. currentmodule:: cantal_tools.werkzeug

Module provides wrapper around werkzeug's BaseWSGIServer.


.. class:: CantaledWSGIServer(\*args, metrics, \**kwargs)

   Wrapper around ``BaseWSGIServer`` from :mod:`werkzeug.serving`

   :param metrics: Metrics instance

   Usage::

      import cantal
      from cantal_tools import Metrics, werkzeug

      metrics = Metrics('my.custom.prefix')
      cantal.start()

      werkzeug.CantaledWSGIServer(
          metrics=metrics,
          host='0.0.0.0',
          port=8080,
          ).server_forever()


Web metrics
-----------

flask
~~~~~

.. currentmodule:: cantal_tools.flask

Module provides Flask application mixin overriding several methods
for request tracing.

.. class:: FlaskMixin(\*args, metrics, \**kwargs)

   Mixin overriding internal application's methods

   :param metrics: Metrics instance

   Usage::

      import flask
      import cantal
      from cantal_tools import Metrics
      from cantal_tools.flask import FlaskMixin

      class App(FlaskMixin, flask.Flask):
          pass

      metrics = Metrics('custom-prefix')
      cantal.start()

      app = App(__name__, metrics=metrics)
      app.run()


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
      from cantal_tools import Metrics
      from cantal_tools.redis import patch_redis

       metrics = Metrics('my-app-prefix')
       cantal.start()

       patch_redis(redis.Redis, metrics=metrics)
       client = Redis(host='localhost', port=6379)
       client.get('some-key')


If you don't like monkey-patching you can use the following connection class,
however you'd need to instantiate :class:`redis.ConnectionPool` by yourself.

.. class:: CantaledConnection(\*args, metrics, \**kwargs)

   Wrapper around :class:`redis.Connection`

----

elasticsearch
~~~~~~~~~~~~~

.. currentmodule:: cantal_tools.elasticsearch

.. class:: CantaledTransport(\*args, metrics, \**kwargs)

   Wrapper around :class:`elasticsearch.Transport`.
   Overrides ``perform_request`` method.

   :param metrics: metrics instance

----

sqlalchemy
~~~~~~~~~~

.. currentmodule:: cantal_tools.sqlalchemy


.. function:: attach_to_engine(engine, metrics)

   Attaches listeners to ``before_cursor_execute`` and ``after_cursor_execute``
   engine events.

   :param engine: SQLAlchemy db engine
   :param metrics: metrics instance

   Usage::

      import cantal
      import sqlalchemy as sa
      from cantal_tools import Metrics
      from cantal_tools.sqlalchemy import attach_to_engine

      metrics = Metrics('my.app')
      cantal.start()

      db_engine = sa.create_engine('sqlite:///db.sqlite')
      attach_to_engine(db_engine, metrics)

----

django
~~~~~~

.. currentmodule:: cantal_tools.django

.. function:: patch_models_manager(django.db.models.Manager)

   Patches supplied django models :class:`django.db.models.Manager` class

   Usage::

      from cantal_tools.django import patch_models_manager
      from django.db import models

      # NOTE: we patch default manager!
      patch_models_manager(models.Manager)
