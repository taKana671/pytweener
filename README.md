# pytweener

This repository provides easing functions implemented in Python.  
I decided to try creative coding with Python and Panda3D, and first created the modules that provide these easing functions as a means to smoothly move animation.
For a demonstration, please see [ParticleText](https://github.com/taKana671/ParticleText).


# Requirements

* Panda3D 1.10.15
* numpy 2.2.4


# Environment

* Python 3.12
* Windows11

# Usage

### Instantiate the Tween class

```
tween = Tween(start, end, duration, delay=0, yoyo=False, easing_type='linear')
```

#### parameters

`start` and `end` can be specified as a scalar, numpy.ndarray, panda3d.core.Point2, Point3, Vec2, Vec3 and so on.

* _start: float_
    * The start point of the animation.

* _end: float_
    * The end point of the animation.

* _duration: int_
    * The time that an animation takes to complete. Specify in seconds.

* _delay: float_
    * Start delay time.

* _yoyo: bool_
    * If True, go to the end point and come back. If False, just go to the end point. The default is False.
            
* _easing_type: string_
    * The function name defined in the Ease class. The default is linear.

### Basic Usage

After instantiating the `Tween class`, call the `start` method. The instance variable `is_playing` is set to `True` when the animation starts and changes to `False` when it ends, and the next move position of the 3D model, etc. is stored in the instance variable `next_pos` after the `update` method is called.

```
from panda3d.core import Point3

from pytweener.tween import Tween

tween = Tween(Point3(0.5, 0.5, 0.5), Point3(3.5, 1.5, 3.5), 2.0, delay=0, yoyo=True, easing_type='in_out_expo')
tween.start()

while True:

    if tween.is_playing:
        tween.update()
        print(tween.next_pos)
    else:
        break

```

#### Loop the animation. 

```
# If the number of repeats is not specified, it loops infinitely.
tween.loop()

# The number of repeats is specified as follows.
#tween.loop(repeats=3)
```

#### Temporarily pause and resume the animation.

```
tween.pause()
tween.resume()
```

#### Stop the animation and move its state to its final state.

```
tween.finish()
```

# References

The easing functions are based on below.
* https://easings.net/.
* http://robertpenner.com/easing/


