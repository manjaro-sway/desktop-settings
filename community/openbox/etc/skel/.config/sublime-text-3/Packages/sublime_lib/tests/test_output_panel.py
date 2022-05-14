import sublime
from sublime_lib import OutputPanel

from unittest import TestCase


class TestOutputPanel(TestCase):

    def setUp(self):
        self.window = sublime.active_window()
        self.panel_to_restore = self.window.active_panel()

        self.panel_name = "test_panel"

    def tearDown(self):
        if getattr(self, 'panel', None):
            self.panel.destroy()

        if self.panel_to_restore:
            self.window.run_command("show_panel", {"panel": self.panel_to_restore})

    def assertContents(self, text):
        view = self.panel.view
        self.assertEqual(
            view.substr(sublime.Region(0, view.size())),
            text
        )

    def test_stream_operations(self):
        self.panel = OutputPanel.create(self.window, self.panel_name)

        self.panel.write("Hello, ")
        self.panel.print("World!")

        self.panel.seek_start()
        self.panel.print("Top")

        self.panel.seek_end()
        self.panel.print("Bottom")

        self.panel.seek(4)
        self.panel.print("After Top")

        self.assertContents("Top\nAfter Top\nHello, World!\nBottom\n")

    def test_clear(self):
        self.panel = OutputPanel.create(self.window, self.panel_name)

        self.panel.write("Some text")
        self.panel.clear()
        self.assertContents("")

    def test_show_hide(self):
        self.panel = OutputPanel.create(self.window, self.panel_name)

        self.panel.show()

        self.assertTrue(self.panel.is_visible())
        self.assertEqual(self.window.active_panel(), self.panel.full_name)

        self.panel.hide()

        self.assertFalse(self.panel.is_visible())
        self.assertNotEqual(self.window.active_panel(), self.panel.full_name)

        self.panel.toggle_visibility()

        self.assertTrue(self.panel.is_visible())
        self.assertEqual(self.window.active_panel(), self.panel.full_name)

        self.panel.toggle_visibility()

        self.assertFalse(self.panel.is_visible())
        self.assertNotEqual(self.window.active_panel(), self.panel.full_name)

    def test_exists(self):
        self.panel = OutputPanel.create(self.window, self.panel_name)
        self.assertIsNotNone(self.window.find_output_panel(self.panel.name))

    def test_destroy(self):
        self.panel = OutputPanel.create(self.window, self.panel_name)
        self.panel.destroy()
        self.assertIsNone(self.window.find_output_panel(self.panel.name))

    def test_settings(self):
        self.panel = OutputPanel.create(self.window, self.panel_name, settings={
            "test_setting": "Hello, World!"
        })

        view_settings = self.panel.view.settings()
        self.assertEqual(view_settings.get("test_setting"), "Hello, World!")

    def test_unlisted(self):
        self.panel = OutputPanel.create(self.window, self.panel_name, unlisted=True)

        self.panel.show()
        self.assertTrue(self.panel.is_visible())
        self.assertNotIn(self.panel.full_name, self.window.panels())

    def test_attach(self):
        self.panel = OutputPanel.create(self.window, self.panel_name, unlisted=True)

        other = OutputPanel(self.window, self.panel_name)
        self.assertEqual(self.panel.view.id(), other.view.id())

        self.panel.destroy()
        with self.assertRaises(ValueError):
            other.tell()

    def test_init_nonexistent_error(self):
        with self.assertRaises(ValueError):
            OutputPanel(self.window, 'nonexistent_output_panel')
