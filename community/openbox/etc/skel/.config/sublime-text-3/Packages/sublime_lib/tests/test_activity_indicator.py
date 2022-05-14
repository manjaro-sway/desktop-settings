from sublime_lib import ActivityIndicator
from sublime_lib.activity_indicator import ViewTarget, WindowTarget

from sublime import View, Window

from unittest import TestCase
from unittest.mock import Mock


class TestActivityIndicator(TestCase):
    def test_window_target(self):
        message = 'Hello, World!'
        window = Mock()
        target = WindowTarget(window)

        target.set(message)
        window.status_message.assert_called_once_with(message)

        window.status_message.reset_mock()
        target.clear()
        window.status_message.assert_called_once_with('')

    def test_view_target(self):
        key = 'test'
        message = 'Hello, World!'
        view = Mock()
        target = ViewTarget(view, key)

        target.set(message)
        view.set_status.assert_called_once_with(key, message)

        target.clear()
        view.erase_status.assert_called_once_with(key)

    def test_init_with_view(self):
        view = View(0)
        indicator = ActivityIndicator(view)
        self.assertIsInstance(indicator._target, ViewTarget)

    def test_init_with_window(self):
        window = Window(0)
        indicator = ActivityIndicator(window)
        self.assertIsInstance(indicator._target, WindowTarget)

    def test_tick(self):
        target = Mock()
        indicator = ActivityIndicator(target)

        results = [
            '[=          ]',
            '[ =         ]',
            '[  =        ]',
            '[   =       ]',
            '[    =      ]',
            '[     =     ]',
            '[      =    ]',
            '[       =   ]',
            '[        =  ]',
            '[         = ]',
            '[          =]',
            '[         = ]',
            '[        =  ]',
            '[       =   ]',
            '[      =    ]',
            '[     =     ]',
            '[    =      ]',
            '[   =       ]',
            '[  =        ]',
            '[ =         ]',
            '[=          ]',
            '[ =         ]',
        ]

        indicator.update()
        for result in results:
            target.set.assert_called_once_with(result)
            target.set.reset_mock()
            indicator.tick()

    def test_label(self):
        target = Mock()
        indicator = ActivityIndicator(target, 'Hello, World!')

        with indicator:
            target.set.assert_called_once_with('Hello, World! [=          ]')

    def test_start_stop(self):
        target = Mock()
        indicator = ActivityIndicator(target)

        indicator.start()
        target.set.assert_called_once_with('[=          ]')
        target.set.reset_mock()

        indicator.stop()
        target.clear.assert_called_once_with()

        indicator.start()
        target.set.assert_called_once_with('[=          ]')

        indicator.stop()

    def test_tick_called(self):
        target = Mock()
        indicator = ActivityIndicator(target)
        with indicator:
            target.set.assert_called_once_with('[=          ]')
            target.set.reset_mock()
            import time
            time.sleep(0.15)
            target.set.assert_called_once_with('[ =         ]')

    def test_start_twice_error(self):
        target = Mock()
        indicator = ActivityIndicator(target)

        with indicator:
            with self.assertRaises(ValueError):
                indicator.start()

    def test_contextmanager(self):
        target = Mock()
        indicator = ActivityIndicator(target)

        with indicator:
            target.set.assert_called_once_with('[=          ]')

        target.clear.assert_called_once_with()
