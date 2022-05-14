import sublime

from .view_stream import ViewStream
from .view_utils import set_view_options, validate_view_options
from ._util.guard import define_guard

from ._compat.typing import Any

__all__ = ['Panel', 'OutputPanel']


class Panel():
    """An abstraction of a panel, such as the console or an output panel.

    :raise ValueError: if `window` has no panel called `panel_name`.

    All :class:`Panel` methods except for :meth:`exists()`
    will raise a ``ValueError`` if the panel does not exist.
    Descendant classes may override :meth:`exists()` to customize this behavior.

    .. py:attribute:: panel_name

        The name of the panel as it is listed in :meth:`sublime.Window.panels()`.

    .. versionadded:: 1.3
    """

    def __init__(self, window: sublime.Window, panel_name: str):
        self.window = window
        self.panel_name = panel_name

        self._checkExists()

    def _checkExists(self) -> None:
        if not self.exists():
            raise ValueError("Panel {} does not exist.".format(self.panel_name))

    @define_guard
    def guard_exists(self) -> None:
        self._checkExists()

    def exists(self) -> bool:
        """Return ``True`` if the panel exists, or ``False`` otherwise.

        This implementation checks :meth:`sublime.Window.panels()`,
        so it will return ``False`` for unlisted panels.
        """
        return self.panel_name in self.window.panels()

    @guard_exists
    def is_visible(self) -> bool:
        """Return ``True`` if the panel is currently visible."""
        return self.window.active_panel() == self.panel_name

    @guard_exists
    def show(self) -> None:
        """Show the panel, hiding any other visible panel."""
        self.window.run_command("show_panel", {"panel": self.panel_name})

    @guard_exists
    def hide(self) -> None:
        """Hide the panel."""
        self.window.run_command("hide_panel", {"panel": self.panel_name})

    @guard_exists
    def toggle_visibility(self) -> None:
        """If the panel is visible, hide it; otherwise, show it."""
        if self.is_visible():
            self.hide()
        else:
            self.show()


class OutputPanel(ViewStream, Panel):
    """
    A subclass of :class:`~sublime_lib.ViewStream` and :class:`~sublime_lib.Panel`
    wrapping an output panel in the given `window` with the given `name`.

    :raise ValueError: if `window` has no output panel called `name`.

    .. versionchanged:: 1.3
        Now a subclass of :class:`Panel`.
    """
    @classmethod
    def create(
        cls,
        window: sublime.Window,
        name: str,
        *,
        force_writes: bool = False,
        follow_cursor: bool = False,
        unlisted: bool = False,
        **kwargs: Any
    ) -> 'OutputPanel':
        """Create a new output panel with the given `name` in the given `window`.

        If `kwargs` are given,
        they will be interpreted as for :func:`~sublime_lib.view_utils.new_view`.
        """
        validate_view_options(kwargs)

        window.destroy_output_panel(name)
        view = window.create_output_panel(name, unlisted)
        set_view_options(view, **kwargs)

        return cls(window, name, force_writes=force_writes, follow_cursor=follow_cursor)

    def __init__(
        self,
        window: sublime.Window,
        name: str,
        *,
        force_writes: bool = False,
        follow_cursor: bool = False
    ):
        view = window.find_output_panel(name)
        if view is None:
            raise ValueError('Output panel "%s" does not exist.' % name)

        ViewStream.__init__(self, view, force_writes=force_writes, follow_cursor=follow_cursor)
        Panel.__init__(self, window, "output." + name)

        self.name = name

    @property
    def full_name(self) -> str:
        """The output panel name, beginning with ``'output.'``.

        Generally, API methods specific to output panels will use :attr:`name`,
        while methods that work with any panels will use :attr:`full_name`.
        """
        return self.panel_name

    def exists(self) -> bool:
        """Return ``True`` if the panel exists, or ``False`` otherwise.

        This implementation checks that the encapsulated :class:`~sublime.View` is valid,
        so it will return ``True`` even for unlisted panels.
        """
        return self.view.is_valid()

    def destroy(self) -> None:
        """Destroy the output panel."""
        self.window.destroy_output_panel(self.name)
