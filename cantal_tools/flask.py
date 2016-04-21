"""This module provides Cantal Flask integration.
"""


class FlaskMixin:
    """Flask App mixin.

    Accepts extra keyword-only argument ``metrics``.
    """

    def __init__(self, *args, metrics, **kw):
        super().__init__(*args, **kw)
        assert hasattr(metrics, 'web'), metrics
        assert hasattr(metrics, 'appflow'), metrics
        self._metrics = metrics

    def wsgi_app(self, environ, start_response):
        with self._metrics.web.context(), self._metrics.appflow.context():
            self._metrics.web.handle_request.enter()
            return super().wsgi_app(environ, start_response)

    def handle_user_exception(self, e):
        self._metrics.web.handle_exception.enter()
        return super().handle_user_exception(e)

    def update_template_context(self, context):
        self._metrics.web.render_template.enter()
        return super().update_template_context(context)
