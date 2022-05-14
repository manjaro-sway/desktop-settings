from threading import Condition, RLock
from contextlib import contextmanager

from types import TracebackType
from .._compat.typing import Optional, TypeVar, Generic, Callable

T = TypeVar('T')

__all__ = ['LockedState']


class LockedState(Generic[T]):
    """A value wrapped in a :class:`threading.Condition`.

    When a thread has acquired the condition,
    no other thread may read or write the state.

    The condition uses a reentrant lock,
    so a thread may acquire it recursively.
    """
    def __init__(self, initial_state: T) -> None:
        self._state = initial_state
        self._condition = Condition(RLock())

    @contextmanager
    def _nonblocking_acquire(self):
        if not self._condition.acquire(blocking=False):
            raise RuntimeError("State cannot be acquired")
        yield
        self._condition.release()

    @property
    def state(self) -> T:
        """The current state.

        When getting or setting the state,
        temporarily acquire the condition without blocking.

        :raise RuntimeError: if the condition cannot be acquired without blocking.
        """
        with self._nonblocking_acquire():
            return self._state

    @state.setter
    def state(self, state: T) -> None:
        with self._nonblocking_acquire():
            self._state = state
            self._condition.notify_all()

    def __enter__(self):
        """Acquire the condition."""
        self._condition.acquire()

    def __exit__(
        self,
        exc_type: type,
        exc_value: Exception,
        traceback: TracebackType
    ) -> None:
        self._condition.release()

    def wait_for(
        self,
        predicate: Callable[[T], bool],
        timeout: Optional[float] = None
    ) -> bool:
        """Wait until the state meets the given `predicate`.

        Return ``True`` unless a given `timeout` expires,
        in which case return ``False``.
        """
        def awaiter():
            with self._condition:
                return predicate(self.state)

        with self._condition:
            return bool(self._condition.wait_for(awaiter, timeout))
