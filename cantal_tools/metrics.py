import time
import cantal
import cantal.fork
from contextlib import contextmanager


class Metrics:
    """All metrics are here."""

    def __init__(self, namespace, extra_branches=()):
        assert isinstance(namespace, str), namespace
        self.wsgi = Fork(
            ('idle', 'acquire', 'process', 'exception'),
            state=namespace + '.wsgi')

        self.web = Fork(
            ('handle_request', 'render_template', 'handle_exception'),
            state=namespace + '.web')

        app_branches = {'redis', 'sqlalchemy', 'elasticsearch'}
        self.appflow = Fork(
            app_branches.union(set(extra_branches)),
            state=namespace + '.appflow')

    def enter_handle_exception(self, *args, **kw):
        self.web.handle_exception.enter()


class Branch(cantal.fork.Branch):

    def exit(self):
        self._parent.exit_branch(self)

    def enter(self, *, end_current=True):
        self._parent.enter_branch(self, end_current=end_current)

    @contextmanager
    def context(self):
        cur_branch = self._parent._branch
        self._parent.enter_branch(self, end_current=False)
        try:
            yield
        finally:
            self.exit()
            if cur_branch:
                cur_branch.enter()

    def _commit(self, start, fin, end=True):
        if end:
            self._counter.incr(1)
        self._duration.incr(fin - start)


class Fork(cantal.fork.Fork):

    def __init__(self, branches, state, **kwargs):
        state_obj = cantal.State(state=state, **kwargs)
        for name in branches:
            setattr(self, name, Branch(name,
                    parent=self, state=state, **kwargs))
        self._state = state_obj
        self._branch = None
        # We do our best not to crash any code which does accouning the
        # wrong way. So to report the problems we use a separate counter
        self._err = cantal.Counter(metric="err", state=state, **kwargs)

    def enter_branch(self, branch, end_current=True):
        ts = int(time.time()*1000)
        if self._branch is not None:
            self._branch._commit(self._timestamp, ts, end=end_current)
        self._state.enter(branch.name, _timestamp=ts)
        self._timestamp = ts
        self._branch = branch

    def exit_branch(self, branch):
        ts = int(time.time() * 1000)
        if self._branch is None:
            self._err.incr()
        branch._commit(self._timestamp, ts)
        self._state.enter('_')
        self._timestamp = ts
        self._branch = None
