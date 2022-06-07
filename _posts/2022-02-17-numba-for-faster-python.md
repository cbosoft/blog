---
layout: post
title: "Numba is crazy awesome"
tags: Python
excerpt: "JIT-compiled python can be <em>incredibly</em> fast. Who says Python can't be performant?"
comments: true
---

# Slow, maths-heavy code.

I have a bit of code which does some maths. It's not particularly important what the maths is for. What is important to note is that the code involves three nested loops around 100 iterations each. 100x100x100 ... that's a lot of loops!

```python
# original.py
import numpy as np


def do_horrid_calc(Na=100, Nb=100, Nc=100):
    P = np.zeros((Na, Nb, Nc))
    angle = np.linspace(0, 1, Nc) * np.pi * 2.0
    L = np.geomspace(1, 1000, Na)
    for i in range(Na):
        for j in range(Nb):
            for k in range(Nc):
                # the actual code is more complex than this,
                # but this gets the point across.
                if angle[k] in [0, np.pi, 2. * np.pi]:
                    P[i, j, k] = np.sqrt(1 - L[i]) * angle[k]
                elif angle[k] in [0, np.pi / 2., 3. * np.pi / 2.]:
                    P[i, j, k] = np.sqrt(2 - L[i]) * angle[k]
                else:
                    P[i, j, k] = np.sqrt(3 - L[i]) * angle[k]
    out = np.trapz(y=P, x=angle, axis=2)
    return L, out
```

This calculation itself needs to be repeated a further 10,000 times, adding to the computational burden.


# Speeding things up

I already use numpy for the maths, as this allows for a decent speed up over pure Python. I'm sure there are simplifications that could be made to the code to improve things, but perhaps there's another way...

## [Numba!](https://numba.pydata.org) (attempt 1)

Numba JIT compiles Python code to improve performance. It even supports (a subset of) numpy!

Great! So just need to `@numba.jit` my calculation and should be good to go.

```python
# naive_numba.py
import numpy as np
import numba


@numba.jit
def do_horrid_calc(Na=100, Nb=100, Nc=100):
    P = np.zeros((Na, Nb, Nc))
    angle = np.linspace(0, 1, Nc) * np.pi * 2.0
    L = np.geomspace(1, 1000, Na)
    for i in range(Na):
        for j in range(Nb):
            for k in range(Nc):
                # the actual code is more complex than this,
                # but this gets the point across.
                if angle[k] in [0, np.pi, 2. * np.pi]:
                    P[i, j, k] = np.sqrt(1 - L[i]) * angle[k]
                elif angle[k] in [np.pi / 2., 3. * np.pi / 2.]:
                    P[i, j, k] = np.sqrt(2 - L[i]) * angle[k]
                else:
                    P[i, j, k] = np.sqrt(3 - L[i]) * angle[k]
    out = np.trapz(y=P, x=angle, axis=2)
    return L, out
```

Running this gives:
```
$ python naive_numba.py
NumbaWarning: 
Compilation is falling back to object mode WITH looplifting enabled because Function "do_horrid_calc" failed type inference due to: Use of unsupported NumPy function 'numpy.geomspace' or unsupported use of the function.

File "naive_numba.py", line 9:
def do_horrid_calc(Na=100, Nb=100, Nc=100):
    <source elided>
    angle = np.linspace(0, 1, Nc) * np.pi * 2.0
    L = np.geomspace(1, 1000, Na)

...

NumbaWarning: 
Compilation is falling back to object mode WITHOUT looplifting enabled because Function "do_horrid_calc" failed type inference due to: No implementation of function Function(<built-in function contains>) found for signature:
 
 >>> contains(Tuple(Literal[int](0), float64, float64), float64)
 
There are 22 candidate implementations:
      - Of which 22 did not match due to:
      Overload of function 'contains': File: <numerous>: Line N/A.
        With argument(s): '(Tuple(int64, float64, float64), float64)':
       No match.
```

Oh, it doesn't like that. This generates a whole bunch of warnings, and numba ends up not compiling the code. It doesn't like my use of the `geomspace` function, and it doesn't like the `angle[k] in [...]` statement.

## Attempt 2
Let's re-factor some things and split the horrible calculation into a public function and an inner function so I can keep using `geomspace`:

```python
# numba_inner_and_public.py
import numpy as np
import numba


@numba.jit
def _horrid_calc_inner(L, Na: int, Nb: int, Nc: int):
    P = np.zeros((Na, Nb, Nc))
    angle = np.linspace(0, 1, Nc) * np.pi * 2.0
    for i in range(Na):
        for j in range(Nb):
            for k in range(Nc):
                # the actual code is more complex than this,
                # but this gets the point across.
                ang_k = angle[k]
                if ang_k == 0.0 or ang_k == np.pi or ang_k == 2.*np.pi:
                    P[i, j, k] = np.sqrt(1 - L[i]) * angle[k]
                elif ang_k == np.pi*.5 or ang_k == np.pi*1.5:
                    P[i, j, k] = np.sqrt(2 - L[i]) * angle[k]
                else:
                    P[i, j, k] = np.sqrt(3 - L[i]) * angle[k]
    out = np.trapz(y=P, x=angle, axis=2)
    return L, out


def do_horrid_calc(Na=100, Nb=100, Nc=100):
    L = np.geomspace(1, 1000, Na)
    return _horrid_calc_inner(L, Na, Nb, Nc)
```

Running this gives:
```
NumbaWarning: 
Compilation is falling back to object mode WITH looplifting enabled because Function "_horrid_calc_inner" failed type inference due to: No implementation of function Function(<function trapz at 0x10bc99ca0>) found for signature:
 
 >>> trapz(y=array(float64, 3d, C), x=array(float64, 1d, C), axis=Literal[int](2))
```

Ahh, number doesn't like `np.trapz` when given an axis parameter (described in docs [here](https://numba.pydata.org/numba-doc/dev/developer/autogen_numpy_listing.html#numpy.trapz)). It seems numba isn't a big fan of n-dimensional arrays! Oh well, can easily move the trapz call out of the inner function.


## Final iteration:

```python
# numba_outer_trapz.py
import numpy as np
import numba


@numba.jit
def _horrid_calc_inner(L, Na: int, Nb: int, Nc: int):
    P = np.zeros((Na, Nb, Nc))
    angle = np.linspace(0, 1, Nc) * np.pi * 2.0
    for i in range(Na):
        for j in range(Nb):
            for k in range(Nc):
                # the actual code is more complex than this,
                # but this gets the point across.
                ang_k = angle[k]
                if ang_k == 0.0 or ang_k == np.pi or ang_k == 2.*np.pi:
                    P[i, j, k] = np.sqrt(1 - L[i]) * angle[k]
                elif ang_k == np.pi*.5 or ang_k == np.pi*1.5:
                    P[i, j, k] = np.sqrt(2 - L[i]) * angle[k]
                else:
                    P[i, j, k] = np.sqrt(3 - L[i]) * angle[k]
    return P, angle


def do_horrid_calc(Na=100, Nb=100, Nc=100):
    L = np.geomspace(1, 1000, Na)
    P, angle = _horrid_calc_inner(L, Na, Nb, Nc)
    out = np.trapz(y=P, x=angle, axis=2)
    return out
```

Runs with no issue!

## So how much faster is the code?

```python
# compare.py
import timeit

from original import do_horrid_calc as original_horrid_calc
from numba_outer_trapz import do_horrid_calc as numba_horrid_calc

fs = dict(
    original=original_horrid_calc,
    numba=numba_horrid_calc
)

for fn, f in fs.items():
    t = timeit.timeit(f, number=100)
    
    print(f'{fn} took {t} s per call')
```

```bash
$ python compare.py
original took 332.914183197 s per call
numba took 1.9284108510000237 s per call
```

### 175 times faster!