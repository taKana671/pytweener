import time
from .ease import Ease


class Tween:
    """A class for Tweening.
        Args:
            start (float):
                The starting point of the animation;
                can be specified as a scalar, numpy.ndarray, panda3d.core.Point2, Point3 and so on.
            end (float):
                The end point of the animation;
                can be specified as a scalar, numpy.ndarray, panda3d.core.Point2, Point3 and so on.
            duration (int): The time that an animation takes to complete; specify in seconds.
            delay (float): start delay time
            yoyo (bool): If true, go to the end point and come back, if false, just go to the end point; default is false.
            easing_type (string): the function name defined in the Ease class; default is linear.
    """

    def __init__(self, start, end, duration, delay=0, yoyo=False, easing_type='linear'):
        self.start_pt = start
        self.end_pt = end
        self._start_pt = start
        self.duration = duration * 1000
        self.delay = delay
        self.yoyo = yoyo

        self.is_playing = False
        self.is_turning_back = False
        self.is_paused = False
        self.pause_start_time = None
        self.do_finish = False
        self.delay_started = False

        self.ease = self.get_ease_func(easing_type)

    def get_ease_func(self, easing_type):
        try:
            ease_func = getattr(Ease, easing_type)
        except AttributeError:
            print(f'not applicable: {easing_type}')
            ease_func = Ease.linear

        return ease_func

    def setup(self, do_loop, repeat):
        self.do_loop = do_loop
        self.repeat = repeat
        self.repeat_cnt = 0
        self.start_time = time.time()
        self.is_playing = True

    def start(self):
        if not self.is_playing:
            self.setup(False, None)

    def delay_start(self, elapsed):
        # if not self.delay_started and elapsed >= self.delay:
        if elapsed >= self.delay:
            # self.delay_started = True
            self.start()

    def loop(self, repeat=None):
        if not self.is_playing:
            self.setup(True, repeat)

    def pause(self):
        if not self.is_paused:
            self.is_paused = True
            self.pause_start_time = time.time()

    def resume(self):
        if self.is_paused:
            pause_duration = time.time() - self.pause_start_time
            self.start_time += pause_duration
            self.is_paused = False

    def finish(self):
        if self.is_playing and not self.is_paused:
            self.do_finish = True

    def turn(self):
        self.start_pt, self.end_pt = self.end_pt, self.start_pt

    def turn_back(self):
        # if not (self.is_playing or self.yoyo or self.do_loop):
        # if not (self.yoyo or self.do_loop):
        self.turn()
        self.start()
            # self.setup(False, None)

    def update(self):
        if self.is_playing and not self.is_paused:
            current_time = time.time()
            elapsed = (current_time - self.start_time) * 1000  # ms
            self.step = min(elapsed / self.duration, 1.0)

            delta = self.end_pt - self.start_pt
            v = self.ease(self.step)
            self.next_pos = delta * v + self.start_pt

            if self.step == 1.0:
                if self.yoyo:
                    self.start_time = current_time
                    self.start_pt, self.end_pt = self.end_pt, self.start_pt

                    if not self.is_turning_back:
                        self.is_turning_back = True
                    else:
                        self.is_turning_back = False

                        if self.do_loop:
                            self.do_continue()
                        else:
                            self.is_playing = False
                else:
                    if self.do_loop:
                        self.start_time = current_time
                        self.do_continue()
                    else:
                        self.is_playing = False

    def do_continue(self):
        if self.do_finish:
            self.is_playing = False
        elif self.repeat:
            if self.repeat_cnt < self.repeat - 1:
                self.repeat_cnt += 1
            else:
                self.is_playing = False