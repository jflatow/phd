"""
Converting Quadratic Polynomials to Quadratic Bezier Curves
===========================================================

Consider that we have a polynomial of the form::

         y(x) = a * (x**2) + b * x + c

However, we want to obtain a curve of the form::

         B(t) = (P0 - 2P1 + P2) * (t**2) - 2 * (P0 + P1) * t + P0

Such a (`Bézier_`) curve is useful in programming graphics,
due to the intuitive interpretation of the parameters `P0`, `P1`, and `P2`::

        It departs from `P0` in the direction of `P1`,
        then bends to arrive at `P2` in the direction from `P1`.
        In other words, the tangents in `P0` and `P2` both pass through `P1`.

.. _Bézier: http://en.wikipedia.org/wiki/Bézier_curve

Suppose we want to draw a portion of the quadratic polynomial function,
starting at point `(xi, y(xi))` and ending at point `(xi + dx, y(xi + dx))`.
If we can solve for the parameters `P0`, `P1`, and `P2` in terms of `xi` and `dx`,
we can use existing functions for drawing quadratic Bézier curves.
For instance, `the quadratic Bézier path commands provided in SVG`__.

.. __: http://www.w3.org/TR/SVG/paths.html#PathDataQuadraticBezierCommands

First, we parameterize the polynomial form by `t`,
so we are comparing apples to apples::

        x(t) = xi + dx * t
        y(t) = a * ((xi + dx * t)**2) + b * (xi + dx * t) + c

If we define that the path should begin at time `t = 0`,
and end at time `t = 1`, clearly::

        P0 = (x(0), y(0)) = (xi, a * (x**2) + b * x + c)
        P2 = (x(1), y(1)) = (xi + dx, a * ((xi + dx)**2) + b * (xi + dx) + c)

Now, since we know the slope of `y(t)`::

        y'(t) = 2 * a * x(t) + b

We can write equations for the tangent lines at `P0` and `P2`::

        y0(t) = y'(0) * x(t) + d0
        y2(t) = y'(1) * x(t) + d2

Using the original equations for `P0` and `P2`,
we can solve for the y-intercepts, `d0` and `d2`::

        d0 = -a * (xi**2) + c
        d2 = -a * ((xi + dx)**2) + c

Finding the intersection of the tangent lines, we have::

        P1 = (xi + dx / 2, a * (xi**2) + b * (xi + dx / 2) + c)

Tada!
"""
from math import factorial

def nchoosek(n, k):
    return factorial(n) / (factorial(k) * factorial(n - k))

class point(tuple):
    def __add__(self, other):
        return point(ps + po for ps, po in zip(self, other))

    def __mul__(self, scalar):
        return point(scalar * p for p in self)

    def __rmul__(self, scalar):
        return self * scalar

class origin(point):
    def __add__(self, other):
        return other

    def __mul__(self, scalar):
        return self

class bezier(tuple):
    def __call__(self, t):
        n = len(self) - 1
        return sum((nchoosek(n, i) * pow(1 - t, n - i) * pow(t, i) * p
                    for i, p in enumerate(self)), origin())

class quadratic(tuple):
    def __call__(self, x):
        return sum(an * pow(x, n) for n, an in enumerate(self))

    def bezier(self, xi, dx):
        c, b, a = self
        return bezier((point((xi, self(xi))),
                       point((xi + dx / 2., a * xi**2 + b * (xi + dx / 2.) + c)),
                       point((xi + dx, self(xi + dx)))))
