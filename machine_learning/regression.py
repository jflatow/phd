from math import exp
from numpy import array, ones, zeros

class Logistic(object):
    def __init__(self, theta):
        self.theta = theta

    def __call__(self, x):
        return 1. / (1. + exp(theta.dot(x)))

def logistic(z):
    return 1. / (1. + exp(-z))

def gl_regression(X, y, h=logistic, N=10000):
    theta = zeros(len(X[0]))
    for k in xrange(1, N):
        for i, x in enumerate(X):
            theta = array([theta[j] + (1. / k) * (y[i] - h(theta.dot(x))) * x_
                           for j, x_ in enumerate(x)])
    return theta
