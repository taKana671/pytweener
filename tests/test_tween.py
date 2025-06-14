import sys
import unittest
from unittest import mock
from io import StringIO

import numpy as np
from panda3d.core import Vec2, Vec3, Point2, Point3

from ..tween import Tween
from ..ease import Ease


# In the upper directory of pytweener, run the test with the following command.
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
        """If an undefined function name is specified, linear is selected.
        """
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


@mock.patch('pytweener.tween.Tween.setup')
class TestStart(unittest.TestCase):
    """tests for Tween.start
    """

    def test_is_playing_true(self, mock_setup):
        tween = Tween(0, 1, 2, easing_type='in_sine')
        tween.is_playing = True

        tween.start()
        mock_setup.assert_not_called()

    def test_is_playing_false(self, mock_setup):
        tween = Tween(0, 1, 2, easing_type='in_sine')
        tween.is_playing = False

        tween.start()
        mock_setup.assert_called_once_with(False, None)


@mock.patch('pytweener.tween.Tween.setup')
class TestLoop(unittest.TestCase):
    """tests for Tween.loop
    """

    def test_is_playing_true(self, mock_setup):
        tween = Tween(0, 1, 2, easing_type='in_sine')
        tween.is_playing = True

        tween.loop()
        mock_setup.assert_not_called()

    def test_is_playing_false(self, mock_setup):
        tween = Tween(0, 1, 2, easing_type='in_sine')
        tween.is_playing = False

        tween.loop(3)
        mock_setup.assert_called_once_with(True, 3)


class TestPause(unittest.TestCase):
    """tests for Tween.pause
    """

    def test_is_paused_true(self):
        tween = Tween(0, 1, 2, easing_type='in_sine')
        tween.is_paused = True
        tween.pause()

        self.assertTrue(tween.is_paused)
        self.assertIsNone(tween.pause_start_time)

    def test_is_paused_false(self):
        tween = Tween(0, 1, 2, easing_type='in_sine')
        self.assertFalse(tween.is_paused)

        with mock.patch('pytweener.tween.time') as mock_time:
            mock_time.time.return_value = 1000
            tween.pause()

        self.assertTrue(tween.is_paused)
        self.assertEqual(tween.pause_start_time, 1000)


@mock.patch('pytweener.tween.time')
class TestResume(unittest.TestCase):
    """tests for Tween.resume
    """

    def test_is_paused_false(self, mock_time):
        tween = Tween(0, 1, 2, easing_type='in_sine')
        tween.is_paused = False
        tween.start_time = 100

        tween.resume()

        mock_time.assert_not_called()
        self.assertEqual(tween.start_time, 100)
        self.assertFalse(tween.is_paused)

    def test_is_paused_true(self, mock_time):
        tween = Tween(0, 1, 2, easing_type='in_sine')
        tween.is_paused = True
        tween.pause_start_time = 120
        tween.start_time = 100

        mock_time.time.return_value = 160
        tween.resume()

        self.assertEqual(tween.start_time, 140)
        self.assertFalse(tween.is_paused)


class TestFinish(unittest.TestCase):
    """tests for Tween.finish
    """

    def test_is_playing_true_is_paused_false(self):
        tween = Tween(0, 1, 2, easing_type='in_sine')
        self.assertFalse(tween.do_finish)
        self.assertFalse(tween.is_paused)
        tween.is_playing = True
        tween.finish()

        self.assertTrue(tween.do_finish)

    def test_other_cases(self):
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


@mock.patch('pytweener.tween.Tween.setup')
class TestTurnBack(unittest.TestCase):
    """tests for Tween.turn_back
    """

    def test_turn_back(self, mock_setup):
        tween = Tween(0, 1, 2, easing_type='in_sine')
        self.assertFalse(tween.yoyo)
        self.assertFalse(tween.is_playing)
        self.assertEqual(tween.start_pt, 0)
        self.assertEqual(tween.end_pt, 1)
        tween.do_loop = False

        tween.turn_back()

        mock_setup.assert_called_once_with(False, None)
        self.assertEqual(tween.start_pt, 1)
        self.assertEqual(tween.end_pt, 0)

    def test_not_turn_back(self, mock_setup):
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

        for is_playing, yoyo, do_loop in tests:
            tween.is_playing = is_playing
            tween.yoyo = yoyo
            tween.do_loop = do_loop
            tween.turn_back()

            mock_setup.assert_not_called()
            self.assertEqual(tween.start_pt, 0)
            self.assertEqual(tween.end_pt, 1)

            mock_setup.reset_mock()


class TestDoContinue(unittest.TestCase):
    """tests for Tween.do_continue
    """

    def test_do_finish(self):
        tween = Tween(0, 1, 2, easing_type='in_sine')

        tests = [
            [True, 3, False],
            [True, None, False],
            [False, None, True]
        ]

        for do_finish, repeat, expect in tests:
            with self.subTest((do_finish, repeat)):
                tween.is_playing = True
                tween.do_finish = do_finish
                tween.repeat = repeat
                tween.do_continue()

                self.assertEqual(tween.is_playing, expect)

    def test_repeat(self):
        tween = Tween(0, 1, 2, easing_type='in_sine')
        self.assertFalse(tween.do_finish)
        tween.is_playing = True
        tween.repeat = 3
        tween.repeat_cnt = 0

        expects = [[1, True], [2, True], [2, False]]

        for expect_cnt, expect_playing in expects:
            with self.subTest():
                tween.do_continue()
                self.assertEqual(tween.repeat_cnt, expect_cnt)
                self.assertEqual(tween.is_playing, expect_playing)


@mock.patch('pytweener.tween.Tween.do_continue')
@mock.patch('pytweener.tween.time')
class TestUpdate(unittest.TestCase):

    def test_update(self, mock_time, _):

        tests = [
            [0, 100, 50],
            [np.array([0, 0, 0]), np.array([100, 100, 100]), np.array([50, 50, 50])],
            [np.array([0, 0]), np.array([100, 100]), np.array([50, 50])],
            [Vec2(0, 0), Point2(100, 100), Vec2(50, 50)],
            [Vec3(0, 0, 0), Vec3(100, 100, 100), Vec3(50, 50, 50)],
            [Point2(0, 0), Point2(100, 100), Point2(50, 50)],
            [Point3(0, 0, 0), Point3(100, 100, 100), Point3(50, 50, 50)]
        ]

        for start, end, expect in tests:
            with self.subTest((start, end)):
                mock_time.time.return_value = 1001

                tween = Tween(0, 100, 2, easing_type='linear')
                tween.is_playing = True
                tween.start_time = 1000
                tween.update()

                if isinstance(expect, np.ndarray):
                    np.testing.assert_array_equal(tween.next_pos, expect)
                else:
                    self.assertEqual(tween.next_pos, expect)

                mock_time.reset_mock()

    def check_value(self, tween, start_pt, end_pt, start_time):
        self.assertEqual(tween.start_pt, start_pt)
        self.assertEqual(tween.end_pt, end_pt)
        self.assertEqual(tween.start_time, start_time)

    def test_yoyo_turn_back(self, mock_time, mock_continue):
        """yoyo: True, do_loop: False or True, is_turning_back: False
        """
        for do_loop in [False, True]:
            with self.subTest(do_loop):
                tween = Tween(0, 100, 2, yoyo=True, easing_type='linear')
                tween.is_playing = True
                tween.start_time = 1000
                tween.do_loop = do_loop
                # the default value of is_tcurnint_back is False.
                self.assertFalse(tween.is_turning_back)

                mock_time.time.return_value = 1002
                tween.update()

                self.assertTrue(tween.is_turning_back)
                self.assertTrue(tween.is_playing)
                self.check_value(tween, start_pt=100, end_pt=0, start_time=1002)
                mock_continue.assert_not_called()

                mock_time.reset_mock()
                mock_continue.reset_mock()

    def test_yoyo_end(self, mock_time, mock_continue):
        """yoyo: True, do_loop: False, is_turning_back: True
        """
        tween = Tween(0, 100, 2, yoyo=True, easing_type='linear')
        tween.is_playing = True
        tween.start_time = 1000
        tween.is_turning_back = True
        tween.do_loop = False

        mock_time.time.return_value = 1002
        tween.update()

        self.assertFalse(tween.is_turning_back)
        self.assertFalse(tween.is_playing)
        self.check_value(tween, start_pt=100, end_pt=0, start_time=1002)
        mock_continue.assert_not_called()

    def test_yoyo_loop(self, mock_time, mock_continue):
        """yoyo: True, do_loop: True, is_turning_back: True
        """
        tween = Tween(0, 100, 2, yoyo=True, easing_type='linear')
        tween.is_playing = True
        tween.start_time = 1000
        tween.is_turning_back = True
        tween.do_loop = True

        mock_time.time.return_value = 1002
        tween.update()

        self.assertFalse(tween.is_turning_back)
        self.assertTrue(tween.is_playing)
        self.check_value(tween, start_pt=100, end_pt=0, start_time=1002)
        mock_continue.assert_called_once()

    def test_not_yoyo_end(self, mock_time, mock_continue):
        """yoyo: Flase, do_loop: False
        """
        tween = Tween(0, 100, 2, easing_type='linear')
        tween.is_playing = True
        tween.start_time = 1000
        tween.do_loop = False

        mock_time.time.return_value = 1002
        tween.update()

        self.assertFalse(tween.is_playing)
        self.check_value(tween, start_pt=0, end_pt=100, start_time=1000)
        mock_continue.assert_not_called()

    def test_not_yoyo_loop(self, mock_time, mock_continue):
        """yoyo: False, do_loop: True
        """
        tween = Tween(0, 100, 2, easing_type='linear')
        tween.is_playing = True
        tween.start_time = 1000
        tween.do_loop = True

        mock_time.time.return_value = 1002
        tween.update()

        self.assertTrue(tween.is_playing)
        self.check_value(tween, start_pt=0, end_pt=100, start_time=1002)
        mock_continue.assert_called_once()
