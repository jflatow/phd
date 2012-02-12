from math import ceil, floor

def nth_root(N, n=3):
    for i in xrange(int(N + 1)):
        if (i + 1) ** n > N:
            return i

def roulette_i(N):
    K = nth_root(N, n=3)
    return sum(3 * n + 4 for n in xrange(1, K)) + N // K - K ** 2 + 1

def roulette(N):
    K = nth_root(N, n=3)
    return (K ** 2 + 5 * K) / 2. - 3 + N // K
