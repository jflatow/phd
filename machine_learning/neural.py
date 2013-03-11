from math import tanh
from random import random

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

class network(list):
    def __init__(self, *shape):
        for i, N in enumerate(shape[:-1]):
            self.append([[random() for _ in xrange(N + 1)] for _ in xrange(shape[i + 1])])

    def forward(self, X):
        Ds, Os = [], [X + [1.]]
        for layer in self:
            Y = [tanh(dot(neuron, Os[-1])) for neuron in layer]
            Ds.append([1 - y * y for y in Y])
            Os.append(Y + [1.])
        return Ds, Os

    def reverse(self, Ds):
        deltas = [Ds[-1]]
        for layer, D in reversed(zip(self[1:] + [[[1.] * len(self[-1])]], Ds[:-1])):
            deltas.insert(0, [di * dot([n[i] for n in layer], deltas[0]) for i, di in enumerate(D)])
        return deltas

    def learn(self, X, T, rate=.05):
        Ds, Os = self.forward(X)
        Ds.append([oi - ti for oi, ti in zip(Os[-1], T)])
        Os.append([di ** 2 / 2. for di in Ds[-1]])
        deltas = self.reverse(Ds)
        for layer, delta, O in zip(self, deltas, Os):
            for i, neuron in enumerate(layer):
                for j, weight in enumerate(neuron):
                    layer[i][j] -= rate * O[j] * delta[i]
        return sum(Os[-1])

    def score(self, X):
        return self.forward(X)[1][-1][:-1]

    def train(self, data, tol=1e-3, **kwds):
        while sum(self.learn(X, T, **kwds) for X, T in data) > tol:
            pass

if __name__ == '__main__':
    xor = [([0,0], [1]), ([0,1], [1]), ([1,0], [1]), ([1,1], [0])]
    net = network(2, 2, 1)
    net.train(xor)
    for pat, exp in xor:
        print pat, exp, net.score(pat)
