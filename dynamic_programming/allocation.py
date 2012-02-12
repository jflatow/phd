
class Allocator(object):
    def __init__(self, a, b, g, h):
        self.a, self.b = a, b
        self.g, self.h = g, h

    def xs(self, x, *ys):
        yield x
        for y in ys:
            x = self.a * y + self.b * (x - y)
            yield x

    def R(self, x, *ys):
        return sum(self.g(yi) + self.h(xi - yi)
                   for xi, yi in zip(self.xs(x, *ys), ys))

    def f(self, N=0):
        """
        maximize over integer values of 0 <= y <= x
        """
        def payoff(x, y):
            p, _y = self.f(N - 1)(self.a * y + self.b * (x - y)) if N else (0, 0)
            return self.g(y) + self.h(x - y) + p
        return lambda x: max((payoff(x, y), y) for y in xrange(int(x + 1)))
