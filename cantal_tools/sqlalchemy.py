from sqlalchemy import event


def attach_to_engine(engine, metrics):

    @event.listens_for(engine, 'before_cursor_execute')
    def enter_db_session(*args, **kw):
        metrics.appflow.sqlalchemy.enter(end_current=False)

    @event.listens_for(engine, 'after_cursor_execute')
    def exit_db_session(*args, **kw):
        # be sure its still sqlalchemy context
        metrics.appflow.sqlalchemy.enter(end_current=False)
        metrics.appflow.sqlalchemy.exit()
