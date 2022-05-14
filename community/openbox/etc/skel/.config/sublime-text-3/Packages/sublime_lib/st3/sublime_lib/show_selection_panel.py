import sublime

from ._util.collections import isiterable
from ._util.named_value import NamedValue
from .flags import QuickPanelOption
from collections.abc import Sequence

from ._compat.typing import Any, Callable, List, Optional, TypeVar, Union, Sequence as _Sequence

_ItemType = TypeVar('_ItemType')

__all__ = ['show_selection_panel', 'NO_SELECTION']


NO_SELECTION = NamedValue('NO_SELECTION')


def show_selection_panel(
    window: sublime.Window,
    items: _Sequence[_ItemType],
    *,
    flags: Any = 0,
    labels: Union[_Sequence[object], Callable[[_ItemType], object]] = None,
    selected: Union[NamedValue, _ItemType] = NO_SELECTION,
    on_select: Optional[Callable[[_ItemType], object]] = None,
    on_cancel: Optional[Callable[[], object]] = None,
    on_highlight: Optional[Callable[[_ItemType], object]] = None
) -> None:
    """Open a quick panel in the given window to select an item from a list.

    :argument window: The :class:`sublime.Window` in which to show the panel.

    :argument items: A nonempty :class:`~collections.abc.Sequence`
        (such as a :class:`list`) of items to choose from.

    Optional keyword arguments:

    :argument flags: A :class:`sublime_lib.flags.QuickPanelOption`,
        a value convertible to :class:`~sublime_lib.flags.QuickPanelOption`,
        or an iterable of such values.

    :argument labels: A value determining what to show as the label for each item:

        - If `labels` is ``None`` (the default), then use `items`.
        - If `labels` is callable, then use ``map(labels, items)``.
        - Otherwise, use `labels`.

        The result should be a :class:`~collections.abc.Sequence` of labels.
        Every label must be a single item
        (a string or convertible with :func:`str`)
        or a :class:`~collections.abc.Sequence` of items.
        In the latter case,
        each entry in the quick panel will show multiple rows.

    :argument selected: The value in `items` that will be initially selected.

        If `selected` is :const:`sublime_lib.NO_SELECTION` (the default),
        then Sublime will determine the initial selection.

    :argument on_select: A callback accepting a value from `items`
        to be invoked when the user chooses an item.

    :argument on_cancel: A callback that will be invoked with no arguments
        if the user closes the panel without choosing an item.

    :argument on_highlight: A callback accepting a value from `items` to be
        invoked every time the user changes the highlighted item in the panel.

    :raise ValueError: if `items` is empty.

    :raise ValueError: if `selected` is given and the value is not in `items`.

    :raise ValueError: if `flags` cannot be converted
        to :class:`sublime_lib.flags.QuickPanelOption`.

    .. versionadded:: 1.2

    .. versionchanged:: 1.3
        `labels` can be a mixture of strings and string sequences of uneven length.

        `flags` can be any value or values
        convertible to :class:`~sublime_lib.flags.QuickPanelOption`.
    """
    if len(items) == 0:
        raise ValueError("The items parameter must contain at least one item.")

    if labels is None:
        labels = items
    elif callable(labels):
        labels = list(map(labels, items))
    elif len(items) != len(labels):
        raise ValueError("The lengths of `items` and `labels` must match.")

    def normalize_label(label: object) -> List[str]:
        if isinstance(label, Sequence) and not isinstance(label, str):
            return list(map(str, label))
        else:
            return [str(label)]

    label_strings = list(map(normalize_label, labels))
    max_len = max(map(len, label_strings))
    label_strings = [rows + [''] * (max_len - len(rows)) for rows in label_strings]

    def on_done(index: int) -> None:
        if index == -1:
            if on_cancel:
                on_cancel()
        elif on_select:
            on_select(items[index])

    if selected is NO_SELECTION:
        selected_index = -1
    else:
        selected_index = items.index(selected)

    on_highlight_callback = None
    if on_highlight:
        on_highlight_callback = lambda index: on_highlight(items[index])

    if isiterable(flags) and not isinstance(flags, str):
        flags = QuickPanelOption(*flags)
    else:
        flags = QuickPanelOption(flags)

    # The signature in the API docs is wrong.
    # See https://github.com/SublimeTextIssues/Core/issues/2290
    window.show_quick_panel(
        items=label_strings,
        on_select=on_done,
        flags=flags,
        selected_index=selected_index,
        on_highlight=on_highlight_callback
    )
