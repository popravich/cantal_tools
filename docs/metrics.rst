Metrics
=======

Common metrics
--------------

Cantal-tools provides following metrics:

   .. attribute:: wsgi
    
      WSGI server group of metrics; contains the following:

      .. attribute:: wsgi.idle

         Idle time and count of wsgi server;

      .. attribute:: wsgi.acquire

         Duration and number of operations of ``socket.acquire`` calls;
            
      .. attribute:: wsgi.process

         Duration and number requests processed;

      .. attribute:: wsgi.exception

         Duration and number of unhandled exceptions processed;

   .. attribute:: web

      Web framework group of metrisc, as follows:

      .. attribute:: web.handle_request

         Duration and number of requests handled;

      .. attribute:: web.render_template

         Duration and number of templates rendered;

      .. attribute:: web.handle_exception

         Duration and number of exceptions processed;

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


Extending common metrics
------------------------

WIP

Custom metrics
--------------

WIP
