from elasticsearch.transport import Transport as _Transport

from .metrics import appflow

__all__ = [
    'CantaledTransport',
    ]

elasticsearch_branch = appflow.ensure_branches('elasticsearch')


class CantaledTransport(_Transport):

    def perform_request(self, method, url, params, body):
        with elasticsearch_branch.context():
            return super(CantaledTransport, self).perform_request(
                method, url, params, body)
