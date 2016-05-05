Metrics
=======

Common metrics
--------------

Cantal-tools provides following metrics:

   .. attribute:: wsgi
    
      WSGI server group of metrics.
      Contains the following:

      .. attribute:: wsgi.idle

         Idle time and count of wsgi server;

      .. attribute:: wsgi.acquire

         Duration and number of operations of ``socket.acquire`` calls;
            
      .. attribute:: wsgi.process

         Duration and number requests processed;

      .. attribute:: wsgi.exception

         Duration and number of unhandled exceptions processed;

      See :ref:`wsgi metrics` for tools & examples using this metrics.

   .. attribute:: web

      Web framework group of metrisc, as follows:

      .. attribute:: web.handle_request

         Duration and number of requests handled;

      .. attribute:: web.render_template

         Duration and number of templates rendered;

      .. attribute:: web.handle_exception

         Duration and number of exceptions processed;

      See :ref:`web metrics` for tools & examples using this metrics.

   .. attribute:: appflow
    
      Application level group of metrics.
      This group of metrics is allowed to extend by developer.

      Basic metrics in this group are:

      .. attribute:: appflow.redis

         Duration and number of redis operations;

      .. attribute:: appflow.sqlalchemy

         Duration and number of SqlAlchemy queries;

      .. attribute:: appflow.elasticsearch

         Duration and number of Elasticsearch queries;

      See :ref:`appflow metrics` for tools & examples using this metrics.


Extending common metrics
------------------------

Existing metrics can be extended with following code:

.. code-block:: python

   # my extra appflow metrics
   import cantal
   import requests
   from cantal_tools.metrics import appflow

   appflow.ensure_branches('external_http', 'upload_file')
   cantal.start()

   def handler(request):
      with appflow.external_http.context():
         requests.get('http://some.host/...')
      with appflow.upload_file.context():
         do_file_upload(request.files)

.. warning::

   Custom branches **MUST** be registered before ``cantal.start()`` call.


Custom metrics
--------------

Custom metrics are just :mod:`cantal` metrics, please see
`cantal's documentation`__ for this.

__ http://cantal-py.readthedocs.org
