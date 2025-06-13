import sys
import unittest
from unittest import mock
from io import StringIO

from ..tween import Tween
from ..ease import Ease

# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# python -m unittest pytweener.tests.test_tween -v


class TestGetEaseFunc(unittest.TestCase):
    """tests for Tween.get_ease_func
    """

    def setUp(self):
        self.capture = StringIO()
        sys.stdout = self.capture

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_failed_get_func(self):
        tween = Tween(0, 1, 2, easing_type='test_func')
        self.assertTrue(tween.ease is Ease.linear)
        self.assertEqual(self.capture.getvalue(), 'not applicable: test_func\n')

    def test_successfully_get_func(self):
        tween = Tween(0, 1, 2, easing_type='out_cubic')
        self.assertTrue(tween.ease is Ease.out_cubic)
        self.assertEqual(self.capture.getvalue(), '')


class TestSetup(unittest.TestCase):
    """tests for Tween.setup
    """

    def test_setup(self):
        tween = Tween(0, 1, 2, easing_type='in_sine')
        self.assertFalse(tween.is_playing)

        with mock.patch('pytweener.tween.time') as mock_time:
            mock_time.time.return_value = 1000
            tween.setup(True, 3)

            self.assertTrue(tween.do_loop)
            self.assertEqual(tween.repeat, 3)
            self.assertEqual(tween.repeat_cnt, 0)
            self.assertEqual(tween.start_time, 1000)
            self.assertTrue(tween.is_playing)


class TestStart(unittest.TestCase):
    """tests for Tween.start
    """

    def test_playing(self):
        tween = Tween(0, 1, 2, easing_type='in_sine')
        tween.is_playing = True

        with mock.patch('pytweener.tween.Tween.setup') as mock_setup:
            tween.start()
            mock_setup.assert_not_called()

    def test_not_playing(self):
        tween = Tween(0, 1, 2, easing_type='in_sine')
        tween.is_playing = False

        with mock.patch('pytweener.tween.Tween.setup') as mock_setup:
            tween.start()
            mock_setup.assert_called_once_with(False, None)


class TestLoop(unittest.TestCase):
    """tests for Tween.loop
    """

    def test_playing(self):
        tween = Tween(0, 1, 2, easing_type='in_sine')
        tween.is_playing = True

        with mock.patch('pytweener.tween.Tween.setup') as mock_setup:
            tween.loop()
            mock_setup.assert_not_called()

    def test_not_playing(self):
        tween = Tween(0, 1, 2, easing_type='in_sine')
        tween.is_playing = False

        with mock.patch('pytweener.tween.Tween.setup') as mock_setup:
            tween.loop(3)
            mock_setup.assert_called_once_with(True, 3)


class TestPause(unittest.TestCase):
    """tests for Tween.pause
    """

    def test_paused(self):
        tween = Tween(0, 1, 2, easing_type='in_sine')
        tween.is_paused = True
        tween.pause()

        self.assertTrue(tween.is_paused)
        self.assertIsNone(tween.pause_start_time)

    def test_not_paused(self):
        tween = Tween(0, 1, 2, easing_type='in_sine')
        self.assertFalse(tween.is_paused)

        with mock.patch('pytweener.tween.time') as mock_time:
            mock_time.time.return_value = 1000
            tween.pause()

        self.assertTrue(tween.is_paused)
        self.assertEqual(tween.pause_start_time, 1000)


class TestResume(unittest.TestCase):
    """tests for Tween.resume
    """

    def test_not_paused(self):
        tween = Tween(0, 1, 2, easing_type='in_sine')
        tween.is_paused = False
        tween.start_time = 100

        with mock.patch('pytweener.tween.time') as mock_time:
            tween.resume()

        mock_time.assert_not_called()
        self.assertEqual(tween.start_time, 100)
        self.assertFalse(tween.is_paused)

    def test_paused(self):
        tween = Tween(0, 1, 2, easing_type='in_sine')
        tween.is_paused = True
        tween.pause_start_time = 120
        tween.start_time = 100

        with mock.patch('pytweener.tween.time') as mock_time:
            mock_time.time.return_value = 160
            tween.resume()

        self.assertEqual(tween.start_time, 140)
        self.assertFalse(tween.is_paused)


class TestFinish(unittest.TestCase):
    """tests for Tween.finish
    """
    def test_finish(self):
        tween = Tween(0, 1, 2, easing_type='in_sine')
        self.assertFalse(tween.do_finish)
        self.assertFalse(tween.is_paused)
        tween.is_playing = True
        tween.finish()

        self.assertTrue(tween.do_finish)

    def test_not_finish(self):
        tween = Tween(0, 1, 2, easing_type='in_sine')
        self.assertFalse(tween.do_finish)

        tests = [
            [True, True],
            [False, True],
            [False, False]
        ]

        for is_playing, is_paused in tests:
            with self.subTest():
                tween.is_playing = is_playing
                tween.is_paused = is_paused
                tween.finish()
                self.assertFalse(tween.do_finish)


class TestTurnBack(unittest.TestCase):
    """tests for Tween.turn_back
    """
    def test_turn_back(self):
        tween = Tween(0, 1, 2, easing_type='in_sine')
        self.assertFalse(tween.yoyo)
        self.assertFalse(tween.is_playing)
        self.assertEqual(tween.start_pt, 0)
        self.assertEqual(tween.end_pt, 1)
        tween.do_loop = False  

        with mock.patch('pytweener.tween.Tween.setup') as mock_setup:
            tween.turn_back()

            mock_setup.assert_called_once_with(False, None)
            self.assertEqual(tween.start_pt, 1)
            self.assertEqual(tween.end_pt, 0)

    def test_not_turn_back(self):
        tween = Tween(0, 1, 2, easing_type='in_sine')
        tests = [
            [True, True, True],
            [True, False, False],
            [True, False, True],
            [True, True, False],
            [False, True, True],
            [False, True, False],
            [False, False, True],
        ]

        with mock.patch('pytweener.tween.Tween.setup') as mock_setup:
            for is_playing, yoyo, do_loop in tests:
                tween.is_playing = is_playing
                tween.yoyo = yoyo
                tween.do_loop = do_loop
                tween.turn_back()

                mock_setup.assert_not_called()
                self.assertEqual(tween.start_pt, 0)
                self.assertEqual(tween.end_pt, 1)
