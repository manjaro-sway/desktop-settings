import sublime

from ._compat.typing import Optional

__all__ = ['new_window', 'close_window']


def new_window(
    *,
    menu_visible: Optional[bool] = None,
    sidebar_visible: Optional[bool] = None,
    tabs_visible: Optional[bool] = None,
    minimap_visible: Optional[bool] = None,
    status_bar_visible: Optional[bool] = None,
    project_data: Optional[dict] = None
) -> sublime.Window:
    """Open a new window, returning the :class:`~sublime.Window` object.

    This function takes many optional keyword arguments:

    :argument menu_visible:
        Show the menubar.
        New windows show the menubar by default.
        On the Mac OS, this argument has no effect.

    :argument sidebar_visible:
        Show the sidebar.
        The sidebar will only be shown
        if the window's project data has at least one folder.

    :argument tabs_visible:
        Show the tab bar.
        If the tab bar is hidden,
        it will not be shown even if there are multiple tabs.

    :argument minimap_visible:
        Show the minimap.

    :argument status_bar_visible:
        Show the status bar.

    :argument project_data:
        Project data for the window, such as `folders`.
        See the `.sublime_project` documentation for details.

    This function currently does not provide a way
    to associate a window with a `.sublime_project` file.

    :raise RuntimeError: if the window is not created for any reason.

    .. versionadded:: 1.2
    """
    original_ids = set(window.id() for window in sublime.windows())

    sublime.run_command('new_window')

    try:
        window = next(window for window in sublime.windows() if window.id() not in original_ids)
    except StopIteration:  # pragma: no cover
        raise RuntimeError("Window not created.") from None

    if menu_visible is not None:
        window.set_menu_visible(menu_visible)

    if sidebar_visible is not None:
        window.set_sidebar_visible(sidebar_visible)

    if tabs_visible is not None:
        window.set_tabs_visible(tabs_visible)

    if minimap_visible is not None:
        window.set_minimap_visible(minimap_visible)

    if status_bar_visible is not None:
        window.set_status_bar_visible(status_bar_visible)

    if project_data is not None:
        window.set_project_data(project_data)

    return window


def close_window(window: sublime.Window, *, force: bool = False) -> None:
    """Close the given window, discarding unsaved changes if `force` is ``True``.

    :raise ValueError: if any view in the window has unsaved changes
        and `force` is not ``True``.

    .. versionadded:: 1.2
    """
    for view in window.views():
        if view.is_dirty() and not view.is_scratch():
            if force:
                view.set_scratch(True)
            else:
                raise ValueError('A view has unsaved changes.')

    window.run_command('close_window')
