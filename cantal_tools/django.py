from functools import wraps

from .metrics import appflow

__all__ = [
    'patch_models_manager',
    ]

appflow.ensure_branches('django_db_get_queryset')


def patch_models_manager(Manager):

    get_queryset = Manager.get_queryset

    @wraps(Manager.get_queryset)
    def _queryset(*args, **kwargs):
        with appflow.django_db_get_queryset.context():
            return get_queryset(*args, **kwargs)

    Manager.get_queryset = _queryset
    return Manager
