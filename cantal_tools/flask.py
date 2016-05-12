"""This module provides Cantal Flask integration.
"""
from werkzeug.exceptions import HTTPException

from .metrics import appflow, web

web.ensure_branches('handle_request', 'handle_exception', 'render_template')


class FlaskMixin(object):
    """Flask App mixin."""

    def wsgi_app(self, environ, start_response):
        with web.context(), appflow.context():
            web.handle_request.enter()
            return super(FlaskMixin, self).wsgi_app(environ, start_response)

    def handle_user_exception(self, e):
        if not isinstance(e, HTTPException):
            web.handle_exception.enter()
        return super(FlaskMixin, self).handle_user_exception(e)

    def update_template_context(self, context):
        web.render_template.enter()
        return super(FlaskMixin, self).update_template_context(context)
