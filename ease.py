import math


class Ease:
    """
    easing functions are based on https://easings.net/.
    # http://robertpenner.com/easing/
    """

    @staticmethod
    def linear(x):
        return x

    @staticmethod
    def in_sine(x):
        """The variable x represents the absolute progress of the animation
           in the bounds of 0 (beginning of the animation) and 1 (end of animation).
        """
        return x if x == 1.0 else 1 - math.cos((x * math.pi) / 2)

    @staticmethod
    def out_sine(x):
        return math.sin((x * math.pi) / 2)

    @staticmethod
    def in_out_sine(x):
        return -(math.cos(math.pi * x) - 1) / 2

    @staticmethod
    def in_cubic(x):
        return math.pow(x, 3)

    @staticmethod
    def out_cubic(x):
        return 1 - math.pow(1 - x, 3)

    @staticmethod
    def in_out_cubic(x):
        return 4 * math.pow(x, 3) if x < 0.5 \
            else 1 - math.pow(-2 * x + 2, 3) / 2

    @staticmethod
    def in_quint(x):
        return math.pow(x, 5)

    @staticmethod
    def out_quint(x):
        return 1 - math.pow(1 - x, 5)

    @staticmethod
    def in_out_quint(x):
        return 16 * math.pow(x, 5) if x < 0.5 \
            else 1 - math.pow(-2 * x + 2, 5) / 2

    @staticmethod
    def in_circ(x):
        return 1 - math.sqrt(1 - math.pow(x, 2))

    @staticmethod
    def out_circ(x):
        return math.sqrt(1 - math.pow(x - 1, 2))

    @staticmethod
    def in_out_circ(x):
        return (1 - math.sqrt(1 - math.pow(2 * x, 2))) / 2 if x < 0.5 \
            else (math.sqrt(1 - math.pow(-2 * x + 2, 2)) + 1) / 2

    @staticmethod
    def in_elastic(x):
        if x == 0.0 or x == 1.0:
            return x

        c4 = math.tau / 3
        return -math.pow(2, 10 * x - 10) * math.sin((x * 10 - 10.75) * c4)

    @staticmethod
    def out_elastic(x):
        if x == 0.0 or x == 1.0:
            return x

        c4 = math.tau / 3
        return math.pow(2, -10 * x) * math.sin((x * 10 - 0.75) * c4) + 1

    @staticmethod
    def in_out_elastic(x):
        if x == 0.0 or x == 1.0:
            return x

        c5 = math.tau / 4.5

        if x < 0.5:
            return -(math.pow(2, 20 * x - 10) * math.sin((20 * x - 11.125) * c5)) / 2

        return math.pow(2, -20 * x + 10) * math.sin((20 * x - 11.125) * c5) / 2 + 1

    @staticmethod
    def in_quad(x):
        return x * x

    @staticmethod
    def out_quad(x):
        return 1 - math.pow(1 - x, 2)

    @staticmethod
    def in_out_quad(x):
        return 2 * x * x if x < 0.5 else 1 - math.pow(-2 * x + 2, 2) / 2

    @staticmethod
    def in_quart(x):
        return math.pow(x, 4)

    @staticmethod
    def out_quart(x):
        return 1 - math.pow(1 - x, 4)

    @staticmethod
    def in_out_quart(x):
        return 8 * math.pow(x, 4) if x < 0.5 else 1 - math.pow(-2 * x + 2, 4) / 2

    @staticmethod
    def in_expo(x):
        return x if x == 0.0 else math.pow(2, 10 * x - 10)

    @staticmethod
    def out_expo(x):
        return x if x == 1.0 else 1 - math.pow(2, -10 * x)

    @staticmethod
    def in_out_expo(x):
        if x == 0.0 or x == 1.0:
            return x

        if x < 0.5:
            return math.pow(2, 20 * x - 10) / 2

        return (2 - math.pow(2, -20 * x + 10)) / 2

    @staticmethod
    def in_back(x):
        if x == 1.0:
            return x

        c1 = 1.70158
        c3 = c1 + 1
        return c3 * math.pow(x, 3) - c1 * math.pow(x, 2)

    @staticmethod
    def out_back(x):
        c1 = 1.70158
        c3 = c1 + 1

        return x if x == 0.0 else 1 + c3 * math.pow(x - 1, 3) + c1 * math.pow(x - 1, 2)

    @staticmethod
    def in_out_back(x):
        c1 = 1.70158
        c2 = c1 * 1.525

        return (math.pow(2 * x, 2) * ((c2 + 1) * 2 * x - c2)) / 2 if x < 0.5 \
            else (math.pow(2 * x - 2, 2) * ((c2 + 1) * (x * 2 - 2) + c2) + 2) / 2

    @staticmethod
    def in_bounce(x):
        return 1 - Ease.out_bounce(1 - x)

    @staticmethod
    def out_bounce(x):
        n1 = 7.5625
        d1 = 2.75

        if x < 1 / d1:
            return n1 * x * x
        elif x < 2 / d1:
            return n1 * math.pow(x - 1.5 / d1, 2) + 0.75
        elif (x < 2.5 / d1):
            return n1 * math.pow(x - 2.25 / d1, 2) + 0.9375
        else:
            return n1 * math.pow(x - 2.625 / d1, 2) * x + 0.984375

    @staticmethod
    def in_out_bounce(x):
        return (1 - Ease.out_bounce(1 - 2 * x)) / 2 if x < 0.5 \
            else (1 + Ease.out_bounce(2 * x - 1)) / 2
