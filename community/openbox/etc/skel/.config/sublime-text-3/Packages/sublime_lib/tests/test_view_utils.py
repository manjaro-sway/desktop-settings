import sublime
from sublime_lib import new_view, close_view, LineEnding

from unittest import TestCase


class TestViewUtils(TestCase):

    def setUp(self):
        self.window = sublime.active_window()

    def tearDown(self):
        if getattr(self, 'view', None):
            try:
                close_view(self.view, force=True)
            except ValueError:
                pass

    def test_new_view(self):
        self.view = new_view(self.window)

        self.assertTrue(self.view.is_valid())

        self.assertEquals(self.view.name(), '')
        self.assertFalse(self.view.is_read_only())
        self.assertFalse(self.view.is_scratch())
        self.assertFalse(self.view.overwrite_status())

        self.assertEquals(self.view.scope_name(0).strip(), 'text.plain')

    def test_name(self):
        self.view = new_view(self.window, name='My Name')

        self.assertEquals(self.view.name(), 'My Name')

    def test_read_only(self):
        self.view = new_view(self.window, read_only=True)

        self.assertTrue(self.view.is_read_only())

    def test_scratch(self):
        self.view = new_view(self.window, scratch=True)

        self.assertTrue(self.view.is_scratch())

    def test_overwrite(self):
        self.view = new_view(self.window, overwrite=True)

        self.assertTrue(self.view.overwrite_status())

    def test_settings(self):
        self.view = new_view(self.window, settings={
            'example_setting': 'Hello, World!',
        })

        self.assertEquals(
            self.view.settings().get('example_setting'),
            'Hello, World!'
        )

    def test_scope(self):
        self.view = new_view(self.window, scope='source.js')

        self.assertTrue(self.view.scope_name(0).startswith('source.js'))

    def test_syntax(self):
        path = 'Packages/JavaScript/JavaScript.sublime-syntax'
        self.view = new_view(self.window, syntax=path)

        self.assertEquals(
            self.view.settings().get('syntax'),
            path
        )

    def test_unknown_args(self):
        self.assertRaises(
            ValueError,
            new_view,
            self.window,
            bogus_arg="Hello, World!"
        )

    def test_syntax_scope_exclusive(self):
        self.assertRaises(
            ValueError,
            new_view,
            self.window,
            scope='source.js',
            syntax='Packages/JavaScript/JavaScript.sublime-syntax'
        )

    def test_encoding(self):
        self.view = new_view(self.window, encoding='utf-16')

        self.assertEquals(self.view.encoding(), "UTF-16 LE with BOM")

    def test_line_endings_unix(self):
        self.view = new_view(self.window, line_endings='unix')

        self.assertEquals(self.view.line_endings(), "Unix")

    def test_line_endings_windows(self):
        self.view = new_view(self.window, line_endings=LineEnding.Windows)

        self.assertEquals(self.view.line_endings(), "Windows")

    def test_line_endings_cr(self):
        self.view = new_view(self.window, line_endings='\r')

        self.assertEquals(self.view.line_endings(), "CR")

    def test_line_endings_invalid(self):
        with self.assertRaises(ValueError):
            self.view = new_view(self.window, line_endings='other')

    def test_content(self):
        self.view = new_view(self.window, content="Hello, World!")

        self.assertEquals(
            self.view.substr(sublime.Region(0, self.view.size())),
            "Hello, World!"
        )

    def test_content_read_only(self):
        self.view = new_view(self.window, content="Hello, World!", read_only=True)

        self.assertEquals(
            self.view.substr(sublime.Region(0, self.view.size())),
            "Hello, World!"
        )

    def test_close_view(self):
        self.view = new_view(self.window)

        close_view(self.view)
        self.assertFalse(self.view.is_valid())

    def test_close_unsaved(self):
        self.view = new_view(self.window, content="Hello, World!")

        self.assertRaises(ValueError, close_view, self.view)
        self.assertTrue(self.view.is_valid())

        close_view(self.view, force=True)
        self.assertFalse(self.view.is_valid())

    def test_close_closed_error(self):
        self.view = new_view(self.window)

        close_view(self.view)
        self.assertRaises(ValueError, close_view, self.view)

    def test_close_panel_error(self):
        view = self.window.create_output_panel('sublime_lib-TestViewUtils')

        self.assertRaises(ValueError, close_view, view)

        self.window.destroy_output_panel('sublime_lib-TestViewUtils')
