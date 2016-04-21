Metrics
=======

Common metrics
--------------

Cantal-tools provides following metrics:

   .. attribute:: Metrics.wsgi
    
      WSGI server group of metrics; contains the following:

      .. attribute:: Metrics.wsgi.idle

         Idle time and count of wsgi server;

      .. attribute:: Metrics.wsgi.acquire

         Duration and number of operations of ``socket.acquire`` calls;
            
      .. attribute:: Metrics.wsgi.process

         Duration and number requests processed;

      .. attribute:: Metrics.wsgi.exception

         Duration and number of unhandled exceptions processed;

   .. attribute:: Metrics.web

      Web framework group of metrisc, as follows:

      .. attribute:: Metrics.web.handle_request

         Duration and number of requests handled;

      .. attribute:: Metrics.web.render_template

         Duration and number of templates rendered;

      .. attribute:: Metrics.web.handle_exception

         Duration and number of exceptions processed;

   .. attribute:: Metrics.appflow
    
      Application level group of metrics.
      This group of metrics is allowed to extend by developer.

      Basic metrics in this group are:

      .. attribute:: Metrics.appflow.redis

         Duration and number of redis operations;

      .. attribute:: Metrics.appflow.sqlalchemy

         Duration and number of SqlAlchemy queries;

      .. attribute:: Metrics.appflow.elasticsearch

         Duration and number of Elasticsearch queries;

Metrics class
-------------

.. currentmodule:: cantal_tools.metrics


.. class:: Metrics(namespace, extra_branches=())

   Is a container for metrics

   :param str namespace: Namespace prefix for metrics
   :param extra_branches: Extra branches to define for ``appflow`` metrics group
   :type extra_branches: :class:`list`, :class:`tuple`

   Basic usage::

      import cantal
      from cantal_tools import Metrics, werkzeug

      metrics = Metrics('my.custom.prefix')
      cantal.start()

      werkzeug.CantaledWSGIServer(
          metrics=metrics,
          host='0.0.0.0',
          port=8080,
          ).server_forever()

   Adding & using extra branches::

      import cantal
      from cantal_tools import Metrics

      metrics = Metrics('my.app', extra_branches=('notify_user'))
      cantal.start()

      def handler(request):
          # do stuff...
          with metrics.appflow.notify_user.context():
              send_some_notification(request)
          # continue doing stuff...

   .. attribute:: wsgi

      Is a :class:`cantal.Fork` instance with following branches:

      * :attr:`Metrics.wsgi.idle`
      * :attr:`Metrics.wsgi.acquire`
      * :attr:`Metrics.wsgi.process`
      * :attr:`Metrics.wsgi.exception`

   .. attribute:: web

      Is a :class:`cantal.Fork` instance with following branches:

      * :attr:`Metrics.web.handle_request`
      * :attr:`Metrics.web.render_template`
      * :attr:`Metrics.web.handle_exception`

   .. attribute:: appflow

      Is a :class:`cantal.Fork` instance with following branches:

      * :attr:`Metrics.appflow.redis`
      * :attr:`Metrics.appflow.sqlalchemy`
      * :attr:`Metrics.appflow.elasticsearch`
