from sublime_lib.encodings import from_sublime, to_sublime

from unittest import TestCase


class TestEncodings(TestCase):

    def test_from(self):
        self.assertEqual(
            from_sublime("Western (Windows 1252)"),
            "cp1252"
        )

    def test_from_error(self):
        with self.assertRaises(ValueError):
            from_sublime("Nonexistent")

    def test_to(self):
        self.assertEqual(
            to_sublime("cp1252"),
            "Western (Windows 1252)"
        )

    def test_to_error(self):
        with self.assertRaises(ValueError):
            to_sublime("Nonexistent")
