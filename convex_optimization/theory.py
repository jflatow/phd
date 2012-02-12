"""
An attempt to codify the relationships between the mathematical objects defined in cvxbook.

Unfortunately, we can't do anything useful, since we sometimes try to enumerate uncountable sets.
However, still a useful exercise, and especially interesting to discover warts in the theory.
For instance, we don't differentiate between points and vectors,
since it is anyways sometimes ambiguous in the book, but always clear from context what is meant.
"""
from itertools import combinations, product

class Reals(object):
    def __init__(self, *dimensions):
        self.dimensions = dimensions

    def __iter__(self):
        pass # wtf does this even mean?
R = Reals(1)

def dot(a, b):
    return sum(a_ * b_ for a_, b_ in zip(a, b))

def pnorm(u, p=2):
    return sum(abs(u_) ** p for u_ in u) ** (1. / p)

def perspective(p):
    return (1. / p[-1] * point(p[:-1]))

class point(tuple):
    def __neg__(self):
        return type(self)(-p for p in self)

    def __add__(self, other):
        return type(self)(ps + po for ps, po in zip(self, other))

    def __sub__(self, other):
        return self + -other

    def __mul__(self, scalar):
        return type(self)(p * scalar for p in self)

    def __rmul__(self, scalar):
        return self * scalar

class origin(point):
    def __add__(self, other):
        return other

    def __radd__(self, other):
        return other

    def __mul__(self, scalar):
        return self
Origin = origin()

class line(set):
    def __init__(self, from_p, thru_p, thetas=R):
        self.from_p = from_p
        self.thru_p = thru_p
        self.thetas = thetas

    def __iter__(self):
        for theta in self.thetas:
            yield theta * self.from_p + (1 - theta) * self.thru_p

class halfspace(set):
    def __init__(self, normal, offset, constraint):
        self.normal = normal
        self.offset = offset
        self.constraint = constraint

    def __iter__(self):
        for point in Reals(len(self.normal)):
            if self.constraint(dot(self.normal, point), self.offset):
                yield point

class hyperplane(halfspace):
    def __init__(self, normal, offset):
        from operator import eq
        super(hyperplane, self).__init__(normal, offset, eq)

class ball(set):
    def __init__(self, center, radius, norm=lambda u: pnorm(u, p=2)):
        self.center = center
        self.radius = radius
        self.norm = norm

    def __iter__(self):
        for point in Reals(len(self.center)):
            if self.norm(point - self.center) <= self.radius:
                yield point

class ellipsoid(set):
    def __init__(self, center, P):
        self.center, P = center, P

    def __iter__(self):
        for point in Reals(len(self.center)):
            # we don't define all of these operations
            if (point - self.center) * inverse(P) * (point - self.center) <= 1:
                yield point

class normcone(set):
    def __init__(self, dimension, norm):
        self.dimension = dimension
        self.norm = norm

    def __iter__(self):
        for point in Reals(self.dimension + 1):
            if self.norm(point[:-1]) <= point[-1]:
                yield point

class polyhedron(set):
    """
    This is just a dummy, since you get a polyhedron if you intersect the other affine sets.
    """

class simplex(polyhedron):
    """
    Just take the convex hull of a set of affinely independent points.
    """

class hull(set):
    def __init__(self, points):
        self.points

class affine(hull):
    def __iter__(self):
        for pair in combinations(self.points, 2):
            for point in line(*pair):
                yield point

def isaffine(set):
    return affine(set) <= set

class convex(hull):
    def __iter__(self):
        for pair in combinations(self.points, 2):
            for point in line(*pair, thetas=(x for x in R if 0 <= x <= 1)):
                yield point

def isconvex(set):
    return convex(set) <= set

class cone(hull):
    """
    According to cvxbook, the conic hull is actually the convex-conic hull (defined below).

    However, in order to maintain symmetry between property tests and hulls,
    we distinguish the two cases here.
    """
    def __iter__(self):
        for _point in self.points:
            for point in line(Origin, _point, thetas=(x for x in R if 0 <= x)):
                yield point

def iscone(set):
    return cone(set) <= set

class convexcone(hull):
    def __iter__(self):
        for pair in combinations(self.points, 2):
            for convexcombo in line(*pair, thetas=(x for x in R if 0 <= x <= 1)):
                for point in line(Origin, convexcombo, thetas=(x for x in R if 0 <= x)):
                    yield point

def isconvexcone(set):
    return convexcone(set) <= set
