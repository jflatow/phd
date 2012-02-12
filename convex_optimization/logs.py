def strval(string):
    return sum(ord(c) * 10**-n for n, c in enumerate(string.lower()))

from itertools import izip
from cvxopt import spmatrix

class Indicator(dict):
    def __init__(self, inverted):
        """
        for key, ids in inverted:
          self[key] = (n, ids)
        """
        super(Indicator, self).__init__((key, (n, ids))
                                        for n, (key, ids) in enumerate(inverted))

    @property
    def matrix(self):
        """
           _          -
        i | 0 | 1  ... |
          |  ...       |
          |_          _|
              j

        feature `i` exists in record `j`
        """
        return spmatrix(1, *izip(*((n, id)
                                   for n, ids in self.itervalues()
                                   for id in ids)))

class Numeric(Indicator):
    @property
    def matrix(self):
        """
           _          -
        i |  val   ... |
          |  ...       |
          |_          _|
              j

        feature `i` takes on value `val` in record `j`
        """
        return spmatrix(*izip(*((val, n, id)
                                for (feature, val), (n, ids) in self.iteritems()
                                for id in ids)))
