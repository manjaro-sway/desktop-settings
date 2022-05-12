import sublime
from sublime_lib import ViewStream

from unittesting import DeferrableTestCase
from io import UnsupportedOperation, StringIO


class TestViewStream(DeferrableTestCase):

    def setUp(self):
        self.view = sublime.active_window().new_file()
        self.stream = ViewStream(self.view)

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.close()

    def assertContents(self, text):
        self.assertEqual(
            self.view.substr(sublime.Region(0, self.view.size())),
            text
        )

    def test_stream_operations(self):
        self.stream.write("Hello, ")
        self.stream.print("World!")
        self.assertEqual(self.stream.tell(), 14)

        self.stream.seek_start()
        self.assertEqual(self.stream.tell(), 0)
        self.stream.print("Top")

        self.stream.seek_end()
        self.assertEqual(self.stream.tell(), 18)
        self.stream.print("Bottom")

        self.stream.seek(4)
        self.stream.print("After Top")

        self.assertContents("Top\nAfter Top\nHello, World!\nBottom\n")

    def test_write_size(self):
        text = "Hello\n\tWorld!"

        size = self.stream.write(text)
        self.assertEqual(size, self.stream.view.size())

    def test_no_indent(self):
        text = "    "

        self.stream.view.settings().set('auto_indent', True)
        self.stream.write(text)
        self.stream.write("\n")
        self.assertContents(text + "\n")

        self.assertTrue(self.stream.view.settings().get('auto_indent'))

    def test_no_indent_off(self):
        text = "    "

        self.stream.view.settings().set('auto_indent', False)
        self.stream.write(text)
        self.stream.write("\n")
        self.assertContents(text + "\n")

        self.assertFalse(self.stream.view.settings().get('auto_indent'))

    def test_clear(self):
        self.stream.write("Some text")
        self.stream.clear()
        self.assertContents("")

    def test_read(self):
        self.stream.write("Hello, World!\nGoodbye, World!")

        self.stream.seek(7)
        text = self.stream.read(5)
        self.assertEqual(text, "World")
        self.assertEqual(self.stream.tell(), 12)

        text = self.stream.read(3)
        self.assertEqual(text, "!\nG")
        self.assertEqual(self.stream.tell(), 15)

        text = self.stream.read(1000)
        self.assertEqual(text, "oodbye, World!")
        self.assertEqual(self.stream.tell(), self.stream.view.size())

        self.stream.seek(7)
        text = self.stream.read(None)
        self.assertEqual(text, "World!\nGoodbye, World!")

        self.stream.seek(7)
        text = self.stream.read(-1)
        self.assertEqual(text, "World!\nGoodbye, World!")

        self.stream.seek(7)
        text = self.stream.read()
        self.assertEqual(text, "World!\nGoodbye, World!")

    def test_readline(self):
        self.stream.write("Hello, World!\nGoodbye, World!")

        self.stream.seek(7)
        text = self.stream.readline()
        self.assertEqual(text, "World!\n")
        self.assertEqual(self.stream.tell(), 14)

        text = self.stream.readline()
        self.assertEqual(text, "Goodbye, World!")

        self.stream.seek(7)
        text = self.stream.readline(1000)
        self.assertEqual(text, "World!\n")
        self.assertEqual(self.stream.tell(), 14)

        self.stream.seek(7)
        text = self.stream.readline(-1)
        self.assertEqual(text, "World!\n")
        self.assertEqual(self.stream.tell(), 14)

        self.stream.seek(7)
        text = self.stream.readline(5)
        self.assertEqual(text, "World")
        self.assertEqual(self.stream.tell(), 12)

    def test_write_read_only_failure(self):
        self.stream.view.set_read_only(True)

        self.assertRaises(ValueError, self.stream.write, 'foo')
        self.assertRaises(ValueError, self.stream.clear)

    def test_write_read_only_success(self):
        self.stream.view.set_read_only(True)
        self.stream.force_writes = True

        self.stream.write('foo')
        self.assertContents('foo')

        self.stream.clear()
        self.assertContents('')

    def _compare_print(self, *args, **kwargs):
        s = StringIO()
        print(*args, file=s, **kwargs)

        self.stream.clear()
        self.stream.print(*args, **kwargs)

        self.assertContents(s.getvalue())

        self.stream.clear()
        print(*args, file=self.stream, **kwargs)

        self.assertContents(s.getvalue())

    def test_print(self):
        text = "Hello, World!"
        number = 42

        self._compare_print(text, number)
        self._compare_print(text, number, sep=',', end=';')
        self._compare_print(text, number, sep='', end='')

    def test_print_no_indent(self):
        text = "    "

        self.stream.view.settings().set('auto_indent', True)
        self.stream.print(text)
        self.assertContents(text + "\n")

    def test_print_read_only_failure(self):
        self.stream.view.set_read_only(True)

        self.assertRaises(ValueError, self.stream.print, 'foo')
        self.assertRaises(ValueError, self.stream.clear)

    def test_print_read_only_success(self):
        self.stream.view.set_read_only(True)
        self.stream.force_writes = True

        self.stream.print('foo')
        self.assertContents("foo\n")

        self.stream.clear()
        self.assertContents('')

    def assertSeek(self, expected, *args):
        returned = self.stream.seek(*args)
        measured = self.stream.tell()
        self.assertEqual(returned, expected)
        self.assertEqual(measured, expected)

    def test_seek(self):
        from io import SEEK_SET, SEEK_CUR, SEEK_END

        self.stream.write('test\n' * 10)

        self.assertSeek(0, -100)
        self.assertSeek(50, 100)
        self.assertSeek(25, 25, SEEK_SET)
        self.assertSeek(35, 10, SEEK_CUR)
        self.assertSeek(0, -100, SEEK_CUR)
        self.assertSeek(50, 0, SEEK_END)
        self.assertSeek(50, 100, SEEK_END)
        self.assertSeek(40, -10, SEEK_END)
        self.assertSeek(0, -100, SEEK_END)

    def test_seek_invalid(self):
        with self.assertRaises(TypeError):
            self.stream.seek(0, -99)

    def assertCursorVisible(self):
        self.assertTrue(
            self.stream.view.visible_region().contains(
                self.stream.tell()
            )
        )

    def test_show_cursor(self):
        self.stream.write('test\n' * 200)

        self.stream.show_cursor()
        yield 200
        self.assertCursorVisible()

    def test_show_cursor_auto(self):
        self.stream.follow_cursor = True

        self.stream.write('test\n' * 200)
        yield 200
        self.assertCursorVisible()

        self.stream.seek_start()
        yield 200
        self.assertCursorVisible()

        self.stream.seek_end()
        yield 200
        self.assertCursorVisible()

    def test_unsupported(self):
        self.assertRaises(UnsupportedOperation, self.stream.detach)

    def test_selection_guard(self):
        sel = self.view.sel()
        sel.clear()
        self.assertRaises(ValueError, self.stream.write, "\n")

        sel.add(0)
        self.stream.write("\n")

        sel.add(0)
        self.assertRaises(ValueError, self.stream.write, "\n")

        sel.clear()
        sel.add(sublime.Region(0, 1))
        self.assertRaises(ValueError, self.stream.write, "\n")

    def test_validity_guard(self):
        self.view.set_scratch(True)
        self.view.close()

        self.assertRaises(ValueError, self.stream.read, None)
        self.assertRaises(ValueError, self.stream.readline)
        self.assertRaises(ValueError, self.stream.write, "\n")
        self.assertRaises(ValueError, self.stream.clear)
        self.assertRaises(ValueError, self.stream.seek, 0)
        self.assertRaises(ValueError, self.stream.seek_start)
        self.assertRaises(ValueError, self.stream.seek_end)
        self.assertRaises(ValueError, self.stream.tell)
        self.assertRaises(ValueError, self.stream.show_cursor)
