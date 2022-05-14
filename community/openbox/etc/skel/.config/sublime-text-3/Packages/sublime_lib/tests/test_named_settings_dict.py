import sublime
from sublime_lib import NamedSettingsDict

import os
from os import path

from unittesting import DeferrableTestCase


class TestNamedSettingsDict(DeferrableTestCase):
    def setUp(self):
        self.name = "_sublime_lib_NamedSettingsDictTest"
        self.fancy = NamedSettingsDict(self.name)
        self.settings_path = path.join(sublime.packages_path(), 'User', self.fancy.file_name)

    def tearDown(self):
        try:
            os.remove(self.settings_path)
        except FileNotFoundError:
            pass

    def test_named(self):
        other = NamedSettingsDict(self.name)

        self.fancy.pop("example_setting", None)
        self.assertNotIn("example_setting", self.fancy)
        self.fancy["example_setting"] = "Hello, World!"

        self.assertIn("example_setting", self.fancy)
        self.assertIn("example_setting", other)

        self.fancy.save()

        yield

        self.assertTrue(path.exists(self.settings_path))

    def test_file_extension(self):
        other = NamedSettingsDict(self.name + '.sublime-settings')

        self.fancy.pop("example_setting", None)
        self.assertNotIn("example_setting", self.fancy)
        self.fancy["example_setting"] = "Hello, World!"
        self.assertEquals(other['example_setting'], 'Hello, World!')
