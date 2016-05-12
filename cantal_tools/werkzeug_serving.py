"""This module provides Cantal-Werkzeug integration."""
import socket

from werkzeug.serving import BaseWSGIServer
from werkzeug.serving import WSGIRequestHandler as _WSGIRequestHandler
from werkzeug.exceptions import InternalServerError
from werkzeug._compat import reraise

from .metrics import wsgi


__all__ = [
    'CantaledWSGIServer',
    ]


wsgi.ensure_branches('idle', 'acquire', 'exception', 'process')


class CantaledWSGIServer(BaseWSGIServer):

    def __init__(self, host, port, app, handler=None,
                 passthrough_errors=False, ssl_context=None, fd=None):
        if handler is not None:
            assert issubclass(handler, WSGIRequestHandler), type(handler)
        else:
            handler = WSGIRequestHandler
        super(CantaledWSGIServer, self).__init__(
            host=host, port=port, app=app,
            handler=handler,
            passthrough_errors=passthrough_errors,
            ssl_context=ssl_context,
            fd=fd)

    def serve_forever(self):
        with wsgi.context():
            wsgi.idle.enter()
            return super(CantaledWSGIServer, self).serve_forever()

    def get_request(self):
        wsgi.acquire.enter()
        return super(CantaledWSGIServer, self).get_request()

    def handle_error(self, request, client_address):
        wsgi.exception.enter()
        return super(CantaledWSGIServer, self).handle_error(
            request, client_address)


class WSGIRequestHandler(_WSGIRequestHandler):

    def setup(self):
        wsgi.process.enter()
        super(WSGIRequestHandler, self).setup()

    def finish(self):
        super(WSGIRequestHandler, self).finish()
        wsgi.idle.enter()

    def run_wsgi(self):
        # XXX: Copy paste of _WSGIRequestHandler.run_wsgi
        #       cause there is no other way to use metrics on error

        if self.headers.get('Expect', '').lower().strip() == '100-continue':
            self.wfile.write(b'HTTP/1.1 100 Continue\r\n\r\n')

        self.environ = environ = self.make_environ()
        headers_set = []
        headers_sent = []

        def write(data):
            assert headers_set, 'write() before start_response'
            if not headers_sent:
                status, response_headers = headers_sent[:] = headers_set
                try:
                    code, msg = status.split(None, 1)
                except ValueError:
                    code, msg = status, ""
                self.send_response(int(code), msg)
                header_keys = set()
                for key, value in response_headers:
                    self.send_header(key, value)
                    key = key.lower()
                    header_keys.add(key)
                if 'content-length' not in header_keys:
                    self.close_connection = True
                    self.send_header('Connection', 'close')
                if 'server' not in header_keys:
                    self.send_header('Server', self.version_string())
                if 'date' not in header_keys:
                    self.send_header('Date', self.date_time_string())
                self.end_headers()

            assert isinstance(data, bytes), 'applications must write bytes'
            self.wfile.write(data)
            self.wfile.flush()

        def start_response(status, response_headers, exc_info=None):
            if exc_info:
                try:
                    if headers_sent:
                        reraise(*exc_info)
                finally:
                    exc_info = None
            elif headers_set:
                raise AssertionError('Headers already set')
            headers_set[:] = [status, response_headers]
            return write

        def execute(app):
            application_iter = app(environ, start_response)
            try:
                for data in application_iter:
                    write(data)
                if not headers_sent:
                    write(b'')
            finally:
                if hasattr(application_iter, 'close'):
                    application_iter.close()
                application_iter = None

        try:
            execute(self.server.app)
        except (socket.error, socket.timeout) as e:
            self.connection_dropped(e, environ)
        except Exception:
            # XXX: all that copy-paste for the sake of this line
            wsgi.exception.enter()

            if self.server.passthrough_errors:
                raise
            from werkzeug.debug.tbtools import get_current_traceback
            traceback = get_current_traceback(ignore_system_exceptions=True)
            try:
                # if we haven't yet sent the headers but they are set
                # we roll back to be able to set them again.
                if not headers_sent:
                    del headers_set[:]
                execute(InternalServerError())
            except Exception:
                print("EXCEPTION IN EXCEPTION")
                pass
            self.server.log('error', 'Error on request:\n%s',
                            traceback.plaintext)
