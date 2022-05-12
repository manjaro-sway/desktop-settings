import sublime
from sublime_lib import Panel

from unittest import TestCase


class TestOutputPanel(TestCase):

    def setUp(self):
        self.window = sublime.active_window()
        self.panel_to_restore = self.window.active_panel()

    def tearDown(self):
        if self.panel_to_restore:
            self.window.run_command("show_panel", {"panel": self.panel_to_restore})

    def test_exists(self):
        panel = Panel(self.window, "console")
        self.assertIn("console", self.window.panels())
        self.assertTrue(panel.exists())

    def test_not_exists(self):
        with self.assertRaises(ValueError):
            Panel(self.window, "nonexistent_panel")

    def test_show_hide(self):
        panel = Panel(self.window, "console")

        panel.show()
        self.assertTrue(panel.is_visible())
        self.assertEqual(self.window.active_panel(), "console")

        panel.hide()
        self.assertFalse(panel.is_visible())
        self.assertNotEqual(self.window.active_panel(), "console")

        panel.show()
        self.assertTrue(panel.is_visible())
        self.assertEqual(self.window.active_panel(), "console")

        panel.toggle_visibility()
        self.assertFalse(panel.is_visible())
        self.assertNotEqual(self.window.active_panel(), "console")

        panel.toggle_visibility()
        self.assertTrue(panel.is_visible())
        self.assertEqual(self.window.active_panel(), "console")
