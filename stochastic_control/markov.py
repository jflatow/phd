"""
Some Markov ideas.

Basic example from: http://www.stanford.edu/class/ee365/lectures/markov.pdf

>>> S = lambda N: ([random.random() > .6 for x in xrange(50)] for _ in xrange(N))
>>> e = monte_carlo(lambda B: B[:25].count(1) / float(B.count(1)) >= .6, S(5000))
>>> .13 < e < .17
True

Inventory example from: http://www.stanford.edu/class/ee365/lectures/markov3.pdf

>>> T = 50
>>> C = 6
>>> X = range(C + 1)
>>> P = {0: {4: .1, 5: .2, 6: .7}, \
         1: {4: .1, 5: .2, 6: .7}, \
         2: {0: .1, 1: .2, 2: .7}, \
         3: {1: .1, 2: .2, 3: .7}, \
         4: {2: .1, 3: .2, 4: .7}, \
         5: {3: .1, 4: .2, 5: .7}, \
         6: {4: .1, 5: .2, 6: .7}}
>>> pi0 = {6: 1}
>>> g = lambda t, x, T: .1 * x + (1 if x <= 1 else 0)
>>> G = lambda t: dict((x, g(t, x, T)) for x in X)

By monte carlo:
>>> S = [list(rwalk(pi0, P, T)) for _ in xrange(1000)]
>>> e = monte_carlo(lambda s: sum(g(t, x, T) for t, x in enumerate(s)), S)
>>> 23 < e < 24
True

By distribution propagation:
>>> pis = [pi0]
>>> for t in xrange(T): pis.append(propf(pis[-1], P))
>>> Js = list(cumsum(dot(pi, G(t)) for t, pi in enumerate(pis)))
>>> abs(Js[-1] - 23.1286) < 1e-4
True
>>> vs = list(values(T, X, P, g))
>>> abs(vs[-1][6] - vs[-2][6] - .446) < 1e-2
True
"""
import itertools
import random

def dot(x, y):
    return sum(x[k] * y.get(k, 0) for k in x)

def irange(N=None):
    return itertools.count() if N is None else xrange(N)

def cumsum(vs, s=0.0):
    for v in vs:
        s += v
        yield s

def cumdist(pi):
    return dict((k, s) for k, s in zip(pi, cumsum(pi.values())))

def sample(pi, N=None):
    def pick(u, c=cumdist(pi)):
        for k, s in c.items():
            if u <= s:
                return k
    for i in irange(N):
        yield pick(random.random())

def estimate(pi, f, N):
    return sum(f(x) for x in sample(pi, N)) / float(N)

def expected(pi, f, X):
    return sum(f(x) * pi.get(x, 0) for x in X)

def probability(pi, E):
    return sum(pi.get(e, 0) for e in E)

def total_variation(pi, pi_):
    return sum(abs(pi.get(k, 0) - pi_.get(k, 0)) for k in set(pi) | set(pi_)) / 2.0

def monte_carlo(f, X):
    for n, e in enumerate(cumsum((f(x) for x in X))):
        pass
    return e / float(n + 1)

def rwalk(pi0, P, T):
    x = next(sample(pi0))
    yield x
    for t in xrange(T):
        x = next(sample(P.get(x, {})))
        yield x

def propf(pi, P):
    pi_ = {}
    for i, p in pi.items():
        for j, q in P.get(i, {}).items():
            pi_[j] = pi_.get(j, 0) + p * q
    return pi_

def propr(P, v):
    return dict((i, dot(p, v)) for i, p in P.items())

def values(T, X, P, g):
    v = dict((x, g(T, x, T)) for x in X)
    yield v
    for t in reversed(xrange(T)):
        r = propr(P, v)
        v = dict((x, g(t, x, T) + r.get(x, 0)) for x in X)
        yield v
