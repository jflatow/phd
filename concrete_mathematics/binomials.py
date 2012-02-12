from itertools import count, islice
from math import factorial
from sums import rising

def product(seq):
    from operator import mul
    return reduce(mul, seq, 1)

class HyperGeometric(object):
    def __init__(self, a_s=(), b_s=()):
        self.a_s = a_s
        self.b_s = b_s

    def __call__(self, z):
        for k in count():
            yield (float(z ** k) / factorial(k) *
                   (product(rising(a, k) for a in self.a_s) /
                    product(rising(b, k) for b in self.b_s)))

    def approx(self, z, k):
        return sum(islice(self(z), k + 1))
