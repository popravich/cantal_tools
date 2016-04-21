"""This module provides Cantal Flask integration.
"""

from .metrics import appflow, web

web.ensure_branches('handle_request', 'handle_exception', 'render_template')


class FlaskMixin:
    """Flask App mixin.

    Accepts extra keyword-only argument ``metrics``.
    """

    def wsgi_app(self, environ, start_response):
        with web.context(), appflow.context():
            web.handle_request.enter()
            return super().wsgi_app(environ, start_response)

    def handle_user_exception(self, e):
        web.handle_exception.enter()
        return super().handle_user_exception(e)

    def update_template_context(self, context):
        web.render_template.enter()
        return super().update_template_context(context)
