from functools import wraps


def patch_models_manager(Manager):

    get_queryset = Manager.get_queryset

    @wraps(Manager.get_queryset)
    def _queryset(*args, **kwargs):
        return get_queryset(*args, **kwargs)

    Manager.get_queryset = _queryset
    return Manager
