import sublime
from sublime_lib import show_selection_panel

from unittest import TestCase
from unittest.mock import NonCallableMagicMock, MagicMock

from inspect import signature


class WindowMock(NonCallableMagicMock):
    def __init__(self, callback=None):
        super().__init__()

        def side_effect(*args, **kwargs):
            bound_args = (signature(sublime.Window.show_quick_panel)
                          .bind(self, *args, **kwargs).arguments)
            callback(**bound_args)

        self.show_quick_panel = MagicMock(
            spec=sublime.Window.show_quick_panel,
            side_effect=side_effect if callback else None
        )


# From Python 3.5
# https://github.com/python/cpython/blob/master/Lib/unittest/mock.py
def assert_not_called(_mock_self):
    """assert that the mock was never called.
    """
    self = _mock_self
    if self.call_count != 0:
        msg = ("Expected '%s' to not have been called. Called %s times.%s"
               % (self._mock_name or 'mock',
                  self.call_count,
                  self._calls_repr()))
        raise AssertionError(msg)


# From Python 3.5
def assert_called_once(_mock_self):
    """assert that the mock was called only once.
    """
    self = _mock_self
    if not self.call_count == 1:
        msg = ("Expected '%s' to have been called once. Called %s times.%s"
               % (self._mock_name or 'mock',
                  self.call_count,
                  self._calls_repr()))
        raise AssertionError(msg)


def assert_called_once_with_partial(mock, **specified_args):
    """Assert that the mock was called once with the specified args, and
    optionally with other args."""
    assert_called_once(mock)
    called_args, called_kwargs = mock.call_args
    called_dict = (signature(sublime.Window.show_quick_panel)
                   .bind(None, *called_args, **called_kwargs).arguments)

    failures = any(
        k in specified_args and v != specified_args[k]
        for k, v in called_dict.items()
    )

    if failures:
        mock.assert_called_once_with(**specified_args)


class TestSelectionPanel(TestCase):
    def test_type_coercion(self):
        window = WindowMock()
        show_selection_panel(
            window=window,
            items=[10, 20, 30],
        )

        assert_called_once_with_partial(
            window.show_quick_panel,
            items=[['10'], ['20'], ['30']],
        )

    def test_multiline_type_coercion(self):
        window = WindowMock()
        show_selection_panel(
            window=window,
            items=[
                ['a', 10],
                ['b', 20],
                ('c', 30),
            ],
        )

        assert_called_once_with_partial(
            window.show_quick_panel,
            items=[
                ['a', '10'],
                ['b', '20'],
                ['c', '30'],
            ],
        )

    def test_empty_items_error(self):
        with self.assertRaises(ValueError):
            show_selection_panel(
                WindowMock(),
                items=[]
            )

    def test_mixed_label_types(self):
        window = WindowMock()
        show_selection_panel(
            window=window,
            items=['a', 'b'],
            labels=[['a'], 'b']
        )

        assert_called_once_with_partial(
            window.show_quick_panel,
            items=[['a'], ['b']],
        )

    def test_mixed_label_lengths(self):
        window = WindowMock()
        show_selection_panel(
            window=window,
            items=['a', 'b'],
            labels=[['a'], ['b', 'c']]
        )

        assert_called_once_with_partial(
            window.show_quick_panel,
            items=[['a', ''], ['b', 'c']],
        )

    def test_item_labels_lengths_error(self):
        with self.assertRaises(ValueError):
            show_selection_panel(
                WindowMock(),
                items=['a', 'b', 'c'],
                labels=['x', 'y']
            )

    def test_selected(self):
        on_select = MagicMock()
        on_cancel = MagicMock()

        show_selection_panel(
            window=WindowMock(lambda on_select, **rest: on_select(1)),
            items=['a', 'b', 'c'],
            on_select=on_select,
            on_cancel=on_cancel
        )
        on_select.assert_called_once_with('b')
        assert_not_called(on_cancel)

    def test_cancel(self):
        on_select = MagicMock()
        on_cancel = MagicMock()

        show_selection_panel(
            window=WindowMock(lambda on_select, **rest: on_select(-1)),
            items=['a', 'b', 'c'],
            on_select=on_select,
            on_cancel=on_cancel
        )
        assert_not_called(on_select)
        on_cancel.assert_called_once_with()

    def test_highlight(self):
        on_highlight = MagicMock()

        show_selection_panel(
            window=WindowMock(lambda on_highlight, **rest: on_highlight(1)),
            items=['a', 'b', 'c'],
            on_highlight=on_highlight,
        )
        on_highlight.assert_called_once_with('b')

    def test_no_flags(self):
        window = WindowMock()

        show_selection_panel(
            window=window,
            items=['a', 'b', 'c']
        )

        assert_called_once_with_partial(
            window.show_quick_panel,
            flags=0
        )

    def test_flags(self):
        window = WindowMock()

        flags = sublime.MONOSPACE_FONT | sublime.KEEP_OPEN_ON_FOCUS_LOST

        show_selection_panel(
            window=window,
            items=['a', 'b', 'c'],
            flags=flags
        )

        assert_called_once_with_partial(
            window.show_quick_panel,
            flags=flags
        )

    def test_flags_conversion(self):
        window = WindowMock()

        flags = ['MONOSPACE_FONT', 'KEEP_OPEN_ON_FOCUS_LOST']

        show_selection_panel(
            window=window,
            items=['a', 'b', 'c'],
            flags=flags
        )

        assert_called_once_with_partial(
            window.show_quick_panel,
            flags=(sublime.MONOSPACE_FONT | sublime.KEEP_OPEN_ON_FOCUS_LOST)
        )

    def test_labels_function(self):
        window = WindowMock()

        show_selection_panel(
            window=window,
            items=[
                {'name': 'a'},
                {'name': 'b'},
                {'name': 'c'},
            ],
            labels=lambda item: item['name']
        )

        assert_called_once_with_partial(
            window.show_quick_panel,
            items=[['a'], ['b'], ['c']],
        )

    def test_labels_list(self):
        window = WindowMock()

        show_selection_panel(
            window=window,
            items=[
                {'name': 'a'},
                {'name': 'b'},
                {'name': 'c'},
            ],
            labels=['a', 'b', 'c'],
        )

        assert_called_once_with_partial(
            window.show_quick_panel,
            items=[['a'], ['b'], ['c']],
        )

    def test_no_selected(self):
        window = WindowMock()

        show_selection_panel(
            window=window,
            items=['a', 'b', 'c'],
        )

        assert_called_once_with_partial(
            window.show_quick_panel,
            selected_index=-1
        )

    def test_selected_simple(self):
        window = WindowMock()

        show_selection_panel(
            window=window,
            items=['a', 'b', 'c'],
            selected='b'
        )

        assert_called_once_with_partial(
            window.show_quick_panel,
            selected_index=1
        )

    def test_selected_complex(self):
        window = WindowMock()

        show_selection_panel(
            window=window,
            items=[
                {'name': 'a'},
                {'name': 'b'},
                {'name': 'c'},
            ],
            labels=lambda item: item['name'],
            selected={'name': 'b'}
        )

        assert_called_once_with_partial(
            window.show_quick_panel,
            selected_index=1
        )

    def test_selected_invalid(self):
        window = WindowMock()

        self.assertRaises(
            ValueError,
            show_selection_panel,
            window=window,
            items=[],
            selected='b'
        )
