"""
Trading example from: http://www.stanford.edu/class/ee365/lectures/trading.pdf
"""
import math
import decision

inf = float('inf')
cut = lambda v, m, M: min(max(v, m), M)

class Trader(decision.MDP):
    def __init__(self, T=250, qmin=-5, qmax=15, gamma=.005, N=20):
        def nprice(p):
            l = 2 * math.log(p)
            a = cut(.4 - l, .01, .98)
            b = cut(.4 + l, .01, .98)
            return {p * (1 + gamma): a, p / (1 + gamma): b, p: 1 - a - b}
        prices = set(reduce(lambda a, b: a + [a[-2] / b, a[-1] * b], [1 + gamma] * N, [1, 1]))
        pdists = dict((p, nprice(p)) for p in prices)
        self.T = T
        self.X = lambda t: [(q, p) for q in range(qmin, qmax) for p in prices]
        self.U = lambda t, (q, p): range(qmin - q, qmax - q + 1)
        self.W = lambda t, (q, p): pdists[p]

    def step(self, t, (q, p), u, p_):
        return q + u, p_

    def cost(self, t, (q, p), u, p_):
        if t < self.T - 1:
            return u * p
        return 0 if q + u == 0 else inf

class TraderSH(Trader):
    def cost(self, t, (q, p), u, p_):
        if t < self.T - 1:
            return u * p + (.005 if q < 0 else 0)
        return 0 if q + u == 0 else inf

class TraderLin(Trader):
    def cost(self, t, (q, p), u, p_):
        if t < self.T - 1:
            return u * p + (.005 * abs(u))
        return 0 if q + u == 0 else inf

class TraderSHNL(Trader):
    def cost(self, t, (q, p), u, p_):
        if t < self.T - 1:
            return u * p + (.0001 if q < 0 else 0) + (.005 * abs(u) ** 1.5)
        return 0 if q + u == 0 else inf

def plot(policy, T=0):
    import mpl_toolkits.mplot3d
    import pylab
    o = policy[T]
    f = pylab.figure()
    a = f.add_subplot(111, projection='3d')
    a.plot_trisurf([q for q, _ in o], [p for _, p in o], [u for v, u in o.values()], cmap=pylab.cm.jet)
    a.set_xlabel('Quantity')
    a.set_ylabel('Price')
    a.set_zlabel('Action')
    pylab.show()

if __name__ == '__main__':
    for trader in (Trader, TraderSH, TraderLin, TraderSHNL):
        plot(dict(trader(T=25).policy()))
