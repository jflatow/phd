from operator import mul
from fractions import Fraction

def delta(f):
    return lambda x: f(x + 1) - f(x)

def shift(f):
    return lambda x: f(x + 1)

def falling(x, m):
    if m < 0:
        return Fraction(1, falling(x - m, -m))
    return reduce(mul, xrange(x, x - m, -1), 1)

def rising(x, m):
    if m < 0:
        return Fraction(1, rising(x + m, -m))
    return reduce(mul, xrange(x, x + m), 1)

