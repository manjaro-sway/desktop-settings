import sublime
from sublime import Region

from contextlib import contextmanager
from io import SEEK_SET, SEEK_CUR, SEEK_END, TextIOBase

from ._util.guard import define_guard

from ._compat.typing import Any, Generator


class ViewStream(TextIOBase):
    """A :class:`~io.TextIOBase` encapsulating a :class:`~sublime.View` object.

    All public methods (except :meth:`flush`) require
    that the underlying View object be valid (using :meth:`View.is_valid`).
    Otherwise, :class:`ValueError` will be raised.

    The :meth:`read`, :meth:`readline`, :meth:`write`, :meth:`print`,
    and :meth:`tell` methods
    require that the underlying View have exactly one selection,
    and that the selection is empty (i.e. a simple cursor).
    Otherwise, :class:`ValueError` will be raised.

    :argument force_writes: If ``True``, then :meth:`write` and :meth:`print`
        will write to the view even if it is read-only.
        Otherwise, those methods will raise :exc:`ValueError`.

    :argument follow_cursor: If ``True``, then any method
        that moves the cursor position will scroll the view
        to ensure that the new position is visible.

    ..  versionchanged:: 1.2
        Added the `follow_cursor` option.
    """

    @define_guard
    @contextmanager
    def guard_read_only(self) -> Generator[Any, None, None]:
        if self.view.is_read_only():
            if self.force_writes:
                self.view.set_read_only(False)
                yield
                self.view.set_read_only(True)
            else:
                raise ValueError("The underlying view is read-only.")
        else:
            yield

    @define_guard
    @contextmanager
    def guard_auto_indent(self) -> Generator[Any, None, None]:
        settings = self.view.settings()
        if settings.get('auto_indent'):
            settings.set('auto_indent', False)
            yield
            settings.set('auto_indent', True)
        else:
            yield

    @define_guard
    def guard_validity(self) -> None:
        if not self.view.is_valid():
            raise ValueError("The underlying view is invalid.")

    @define_guard
    def guard_selection(self) -> None:
        if len(self.view.sel()) == 0:
            raise ValueError("The underlying view has no selection.")
        elif len(self.view.sel()) > 1:
            raise ValueError("The underlying view has multiple selections.")
        elif not self.view.sel()[0].empty():
            raise ValueError("The underlying view's selection is not empty.")

    def __init__(
        self, view: sublime.View, *, force_writes: bool = False, follow_cursor: bool = False
    ):
        self.view = view
        self.force_writes = force_writes
        self.follow_cursor = follow_cursor

    @guard_validity
    @guard_selection
    def read(self, size: int = -1) -> str:
        """Read and return at most `size` characters from the stream as a single :class:`str`.

        If `size` is negative or None, read until EOF.
        """
        begin = self._tell()
        end = self.view.size()

        if size is None:
            size = -1

        return self._read(begin, end, size)

    @guard_validity
    @guard_selection
    def readline(self, size: int = -1) -> str:
        """Read and return one line from the stream, to a maximum of `size` characters.

        If the stream is already at EOF, return an empty string.
        """
        begin = self._tell()
        end = self.view.full_line(begin).end()

        return self._read(begin, end, size)

    def _read(self, begin: int, end: int, size: int) -> str:
        if size >= 0:
            end = min(end, begin + size)

        self._seek(end)
        return self.view.substr(Region(begin, end))

    @guard_validity
    @guard_selection
    @guard_read_only
    @guard_auto_indent
    def write(self, s: str) -> int:
        """Insert the string `s` into the view immediately before the cursor
        and return the number of characters inserted.

        Because Sublime may convert tabs to spaces,
        the number of characters inserted may not match
        the length of the argument.
        """
        old_size = self.view.size()
        self.view.run_command('insert', {'characters': s})
        self._maybe_show_cursor()
        return self.view.size() - old_size

    def print(self, *objects: object, sep: str = ' ', end: str = '\n') -> None:
        """Shorthand for :func:`print()` passing this ViewStream as the `file` argument."""
        print(*objects, file=self, sep=sep, end=end)  # type: ignore

    def flush(self) -> None:
        """Do nothing. (The stream is not buffered.)"""
        pass

    @guard_validity
    def seek(self, offset: int, whence: int = SEEK_SET) -> int:
        """Move the cursor in the view and return the new offset.

        If `whence` is provided,
        the behavior is the same as for :class:`~io.IOBase`.
        If the cursor would move before the beginning of the view,
        it will move to the beginning instead,
        and likewise for the end of the view.
        If the view had multiple selections, none will be preserved.

        ..  versionchanged:: 1.2
            Allow non-zero arguments with any value of `whence`.
        """
        if whence == SEEK_SET:
            return self._seek(offset)
        elif whence == SEEK_CUR:
            return self._seek(self._tell() + offset)
        elif whence == SEEK_END:
            return self._seek(self.view.size() + offset)
        else:
            raise TypeError('Invalid value for argument "whence".')

    def _seek(self, offset: int) -> int:
        selection = self.view.sel()
        selection.clear()
        selection.add(Region(offset))
        self._maybe_show_cursor()
        return self._tell()

    @guard_validity
    def seek_start(self) -> None:
        """Move the cursor in the view to before the first character."""
        self._seek(0)

    @guard_validity
    def seek_end(self) -> None:
        """Move the cursor in the view to after the last character."""
        self._seek(self.view.size())

    @guard_validity
    @guard_selection
    def tell(self) -> int:
        """Return the character offset of the cursor."""
        return self._tell()

    def _tell(self) -> int:
        return self.view.sel()[0].b

    @guard_validity
    @guard_selection
    def show_cursor(self) -> None:
        """Scroll the view to show the position of the cursor."""
        self._show_cursor()

    def _show_cursor(self) -> None:
        self.view.show(self._tell())

    def _maybe_show_cursor(self) -> None:
        if self.follow_cursor:
            self._show_cursor()

    @guard_validity
    @guard_selection
    @guard_read_only
    def clear(self) -> None:
        """Erase all text in the view."""
        self.view.run_command('select_all')
        self.view.run_command('left_delete')
