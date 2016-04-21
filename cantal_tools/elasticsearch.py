from elasticsearch.transport import Transport as _Transport


__all__ = [
    'CantaledTransport',
    ]


class CantaledTransport(_Transport):

    def __init__(self, *args, metrics, **kwargs):
        super().__init__(*args, **kwargs)
        self._branch = metrics.appflow.elasticsearch

    def perform_request(self, method, url, params, body):
        with self._branch.context():
            return super().perform_request(method, url, params, body)
