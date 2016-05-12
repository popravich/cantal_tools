"""This module provides wrapped Redis client."""

import redis
from functools import wraps

from .metrics import appflow

__all__ = [
    'patch_redis',
    'CantaledConnection',
    ]

appflow.ensure_branches('redis')


def patch_redis(redis):
    """Wraps `execute_command` method."""
    real_func = redis.execute_command

    @wraps(real_func)
    def execute_with_metrics(*args, **options):
        with appflow.redis.context():
            return real_func(*args, **options)

    redis.execute_command = execute_with_metrics
    return redis


class CantaledConnection(redis.Connection):

    def execute_command(self, *args, **options):
        with appflow.redis.context():
            return super(CantaledConnection, self).execute_command(
                *args, **options)
