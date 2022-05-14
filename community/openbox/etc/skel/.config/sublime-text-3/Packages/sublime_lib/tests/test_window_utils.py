import sublime
from unittest import skipIf
from unittesting import DeferrableTestCase

from sublime_lib import new_window, close_window


class TestNewWindow(DeferrableTestCase):

    def tearDown(self):
        if getattr(self, '_window', None):
            close_window(self._window, force=True)

    def test_is_valid(self):
        self._window = new_window()
        self.assertTrue(self._window.is_valid())

    def test_has_view(self):
        self._window = new_window()
        self.assertIsNotNone(self._window.active_view())

    def test_close_window(self):
        self._window = new_window()
        close_window(self._window)
        yield 500
        self.assertFalse(self._window.is_valid())

    def test_close_unsaved(self):
        self._window = new_window()

        self._window.active_view().run_command('insert', {'characters': 'Hello, World!'})

        with self.assertRaises(ValueError):
            close_window(self._window)

        close_window(self._window, force=True)
        yield 500
        self.assertFalse(self._window.is_valid())

    def test_menu_visible(self):
        self._window = new_window(menu_visible=True)
        self.assertTrue(self._window.is_menu_visible())

    @skipIf(sublime.platform() == 'osx', "Menus are always visible on Mac OS.")
    def test_menu_not_visible(self):
        self._window = new_window(menu_visible=False)
        self.assertFalse(self._window.is_menu_visible())

    def test_sidebar_visible(self):
        self._window = new_window(sidebar_visible=True)
        self.assertTrue(self._window.is_sidebar_visible())

    def test_sidebar_not_visible(self):
        self._window = new_window(sidebar_visible=False)
        self.assertFalse(self._window.is_sidebar_visible())

    def test_tabs_visible(self):
        self._window = new_window(tabs_visible=True)
        self.assertTrue(self._window.get_tabs_visible())

    def test_tabs_not_visible(self):
        self._window = new_window(tabs_visible=False)
        self.assertFalse(self._window.get_tabs_visible())

    def test_minimap_visible(self):
        self._window = new_window(minimap_visible=True)
        self.assertTrue(self._window.is_minimap_visible())

    def test_minimap_not_visible(self):
        self._window = new_window(minimap_visible=False)
        self.assertFalse(self._window.is_minimap_visible())

    def test_status_bar_visible(self):
        self._window = new_window(status_bar_visible=True)
        self.assertTrue(self._window.is_status_bar_visible())

    def test_status_bar_not_visible(self):
        self._window = new_window(status_bar_visible=False)
        self.assertFalse(self._window.is_status_bar_visible())

    def test_project_data(self):
        data = {
            'folders': [
                {'path': sublime.packages_path()},
            ],
        }

        self._window = new_window(project_data=data)
        self.assertEqual(
            self._window.project_data(),
            data
        )
