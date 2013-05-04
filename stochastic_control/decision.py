"""
Bellman equations for random variables (Markov Decision Problems)

Examples from: http://www.stanford.edu/class/ee365/lectures/dp.pdf

Our old friend, inventory:

>>> inf = float('inf')
>>> T = 50
>>> C = 6
>>> X = lambda t: range(C + 1)
>>> mdp = MDP(T, X, W=lambda t, x, u: {0: .7, 1: .2, 2: .1})
>>> mdp.step = lambda t, x, u, d: x - d + u
>>> mdp.cost = lambda t, x, u, d: .1 * x + 1 * (u > 0) if 0 <= x - d + u <= C else inf
>>> mu = dict(mdp.policy())
>>> [t for t, p in mu.items() if [u for x, (v, u) in p.items()] == [4, 3, 0, 0, 0, 0, 0]] == range(T - 2)
True
"""

class MDP(object):
    def __init__(self, T, X, U=None, W=None):
        self.T = T
        self.X = X
        self.U = U or (lambda t, x: X(t))
        self.W = W or (lambda t, x, u: {None: 1})

    def step(self, t, x, u, w):
        """Return the state at time t + 1."""

    def cost(self, t, x, u, w):
        """Return a real or infinite stage cost."""

    def policy(self, p={}):
        f = self.step
        g = self.cost
        E = lambda t, x, u, W: sum((g(t, x, u, w) + V(t, f(t, x, u, w))) * p for w, p in W.items())
        V = lambda t, x: p.get(x, (0, None))[0]
        for t in reversed(xrange(self.T)):
            p = dict((x, min((E(t, x, u, self.W(t, x, u)), u) for u in self.U(t, x))) for x in self.X(t))
            yield t, p
