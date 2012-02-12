
def args(f):
    return f.__code__.co_varnames

def nargs(f):
    return f.__code__.co_argcount

class limit(object):
    """
    As the input to `f` comes arbitrarily close to `c`,
    the output of `f` becomes arbitrarily close to this.
    """
    def __init__(self, f, c):
        self.f = f
        self.c = c

class derivative(object):
    """
    A measure of the change in the output of a function w.r.t. its input.
    """
    def __init__(self, f):
        self.f = f

class partial(derivative):
    """
    A measure of the change in the output of a function w.r.t. one of its inputs,
    while holding the others constant.
    """
    def __init__(self, f, i):
        super(partial, self).__init__(f)
        self.i = i

    def __call__(self, *args):
        return limit(lambda h: (self.f(*[arg + h if i == self.i else arg
                                         for i, arg in enumerate(args)]) -
                                self.f(*args)) / h, 0)

    @property
    def __code__(self):
        return self.f.__code__

    @property
    def __name__(self):
        return '\u2202%s/\u2202%s' % (self.f.__name__, args(self.f)[self.i])

    def __repr__(self):
        return self.__name__

def gradient(y):
    return [partial(y, i) for i in range(nargs(y))]

def hessian(y):
    return jacobian(gradient(y))

def jacobian(Y):
    return [gradient(y) for y in Y]

