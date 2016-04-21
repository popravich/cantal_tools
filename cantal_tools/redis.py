"""This module provides wrapped Redis client."""

import redis
from functools import wraps


__all__ = [
    'patch_redis',
    'CantaledConnection',
    ]


def patch_redis(redis, metrics):
    real_func = redis.execute_command

    @wraps(real_func)
    def execute_with_metrics(*args, **options):
        with metrics.appflow.redis.context():
            return real_func(*args, **options)

    redis.execute_command = execute_with_metrics
    return redis


class CantaledConnection(redis.Connection):

    def __init__(self, *args, metrics, **kwargs):
        super().__init__(*args, **kwargs)
        self._branch = metrics.appflow.redis

    def execute_command(self, *args, **options):
        with self._branch.context():
            return super().execute_command(*args, **options)
