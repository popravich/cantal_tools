from sqlalchemy import event

from .metrics import appflow

__all__ = [
    'attach_to_engine',
    ]

sqlalchemy_branch = appflow.ensure_branches('sqlalchemy')


def attach_to_engine(engine):

    @event.listens_for(engine, 'before_cursor_execute')
    def enter_db_session(*args, **kw):
        sqlalchemy_branch.enter(end_current=False)

    @event.listens_for(engine, 'after_cursor_execute')
    def exit_db_session(*args, **kw):
        # be sure its still sqlalchemy context
        sqlalchemy_branch.enter(end_current=False)
        sqlalchemy_branch.exit()
