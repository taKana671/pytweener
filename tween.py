import time
from enum import StrEnum, auto, Enum
from .ease import Ease



# class Easing(Enum):

#     SINE = auto()
#     CUBIC = auto()
#     QUINT = auto()
#     CIRC = auto()
#     ELASTIC = auto()
#     QUAD = auto()
#     QUART = auto()
#     EXPO = auto()
#     BACK = auto()
#     BOUNCE = auto()


# class Mode(StrEnum):

#     IN = auto()
#     OUT = auto()
#     IN_OUT = auto()


# EasingType = StrEnum(
#     'EasingType',
#     [(f'{f.name}_{m.name}', auto()) for f in Mode for m in Easing]
# )


Easing = [
    'SINE',
    'CUBIC',
    'QUINT',
    'CIRC',
    'ELASTIC',
    'QUAD',
    'QUART',
    'EXPO',
    'BACK',
    'BOUNCE'
]

Mode = [
    'IN',
    'OUT',
    'IN_OUT'
]

EasingType = StrEnum(
    'EasingType',
    [(f'{f}_{m}', auto()) for f in Mode for m in Easing]
)


class Tween:

    # def __init__(self, start, end, duration, repeat=None, loop=False, yoyo=False, easing_type='linear'):
    def __init__(self, start, end, duration, yoyo=False, easing_type='linear'):
        self.start_pt = start
        self.end_pt = end
        self._start_pt = start

        self.duration = duration * 1000
        self.yoyo = yoyo
        # self.loop = loop
        # self.repeat = repeat
        # self.repeat_cnt = 0

        self.is_playing = False
        self.is_turning_back = False

        self.is_paused = False
        self.pause_start_time = None

        self.do_finish = False

        self.ease = self.get_ease_func(easing_type)

    def get_ease_func(self, easing_type):
        try:
            ease_func = getattr(Ease, easing_type)
        except AttributeError:
            raise
        else:
            return ease_func

    def setup(self, do_loop, repeat):
        if not self.is_playing:
            self.repeat = repeat
            self.repeat_cnt = 0
            self.do_loop = do_loop

            self.start_time = time.time()
            self.is_playing = True

    def start(self):
        self.setup(False, None)

        # if not self.is_playing:
        #     self.is_playing = True
        #     self.start_time = time.time()

    def loop(self, repeat=None):
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

    def turn_back(self):
        pass

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
                    if not self.is_turning_back:
                        self.start_time = current_time
                        self.start_pt, self.end_pt = self.end_pt, self.start_pt
                        self.is_turning_back = True

                    else:
                        self.is_turning_back = False

                        if self.do_finish:
                            self.is_playing = False

                        elif self.do_loop:
                            if self.repeat:
                                if self.repeat_cnt < self.repeat - 1:
                                    self.repeat_cnt += 1
                                    self.start_time = current_time
                                    self.start_pt, self.end_pt = self.end_pt, self.start_pt
                                else:
                                    self.is_playing = False
                            else:
                                self.start_time = current_time
                                self.start_pt, self.end_pt = self.end_pt, self.start_pt
                        else:
                            self.is_playing = False

                else:
                    if self.do_finish:
                        self.is_playing = False

                    elif self.do_loop:
                        if self.repeat:
                            if self.repeat_cnt < self.repeat - 1:
                                self.repeat_cnt += 1
                                self.start_time = current_time
                            else:
                                self.is_playing = False
                        else:
                            self.start_time = current_time
                    else:
                        self.is_playing = False

        # print(self.repeat, self.repeat_cnt)                   





            # print(self.start_pt, self.end_pt, delta * v, delta * v + self.start_pt)
            # return delta * v + self.start_pt