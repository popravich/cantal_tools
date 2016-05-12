import time
import cantal

from cantal import fork
from contextlib import contextmanager


class Branch(fork.Branch):
    __slots__ = fork.Branch.__slots__

    def __init__(self, suffix, state, parent, **kwargs):
        super(Branch, self).__init__(suffix, state, parent, **kwargs)
        self._errors = cantal.Counter(state=state + '.' + suffix,
                                      metric='errors', **kwargs)

    def exit(self):
        self._parent.exit_branch(self)

    def enter(self, end_current=True):
        self._parent.enter_branch(self, end_current=end_current)

    @contextmanager
    def context(self):
        cur_branch = self._parent._branch
        self._parent.enter_branch(self, end_current=False)
        try:
            yield
        except Exception:
            self._errors.incr(1)
            raise
        finally:
            self.exit()
            if cur_branch:
                cur_branch.enter()

    def _commit(self, start, fin, increment=True):
        if increment:
            self._counter.incr(1)
        self._duration.incr(fin - start)


class Fork(fork.Fork):
    """Custom Fork class without branches argument, instead
    ensure_branch must be used.
    """

    def __init__(self, state, **kwargs):
        self._state = cantal.State(state=state, **kwargs)
        self._kwargs = kwargs
        self._kwargs['state'] = state
        self._branch = None
        # We do our best not to crash any code which does accouning the
        # wrong way. So to report the problems we use a separate counter
        self._err = cantal.Counter(metric="err", **self._kwargs)

    def enter_branch(self, branch, end_current=True):
        ts = int(time.time()*1000)
        if self._branch is not None:
            self._branch._commit(self._timestamp, ts, increment=end_current)
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

    def ensure_branches(self, *branches):
        ret = []
        for name in branches:
            branch = getattr(self, name, None)
            assert branch is None or isinstance(branch, Branch), (name, branch)
            if branch is None:
                branch = Branch(name, parent=self, **self._kwargs)
                setattr(self, name, branch)
            ret.append(branch)
        if len(branches) == 1:
            return ret[0]
        return ret
