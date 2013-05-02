"""
Active query example from: http://www.stanford.edu/class/ee365/lectures/active_query.pdf
"""
import decision

class Designer(decision.MDP):
    tests = [(.25, .10, 2),
             (.10, .20, 3),
             (.05, .05, 7),
             (.50, .50, 0)]

    def __init__(self, T=3, prior=.6, rho=100, N=1000):
        Q = [{0: {0: 1 - a, 1: a},
              1: {0: b, 1: 1 - b}}
             for a, b, c in self.tests]
        def transition(p, q):
            pi = {}
            for y in (0, 1):
                b = q[0][y] * (1 - p) + q[1][y] * p
                f = q[1][y] * p / b
                n = int(f * N)
                pi[n] = pi.get(n, 0) + b
            return pi
        self.ptrans = ptrans = dict(((n, k), transition(n / float(N), Q[k]))
                                    for n in range(N + 1)
                                    for k in range(len(self.tests)))
        self.r = rho / float(N)
        self.N = N
        self.T = T
        self.X = lambda t: range(N + 1)
        self.U = lambda t, n: range(len(self.tests))
        self.W = lambda t, n, k: ptrans[n, k]

    def step(self, t, n, k, n_):
        return n_

    def cost(self, t, n, k, n_):
        if t < self.T - 1:
            return self.tests[k][2]
        return self.tests[k][2] + self.r * min(n_, self.N - n_)

def plot(policy, T=0):
    import mpl_toolkits.mplot3d
    import pylab
    f = pylab.figure()
    o = policy[T]
    a = f.add_subplot(111, projection='3d')
    a.scatter([n for n in o], [u for v, u in o.values()], [v for v, u in o.values()], alpha=.1)
    a.set_title('T = %s' % T)
    a.set_xlabel('State')
    a.set_ylabel('Test')
    a.set_zlabel('Cost')
    pylab.show()

if __name__ == '__main__':
    designer = Designer()
    policy = dict(designer.policy())
    for t in range(designer.T):
        plot(policy, t)
