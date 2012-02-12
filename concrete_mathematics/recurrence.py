def hanoi(n):
    return 2 ** n - 1

def hanoi_r(n):
    if n == 0:
        return 0
    return 2 * hanoi_r(n - 1) + 1

def josephus(n):
    return ((n << 1) & ((1 << n.bit_length()) - 1)) + 1

def josephus_r(n):
    if n <= 1:
        return 1
    return 2 * josephus_r(n / 2) + (n % 2 or -1)

def f(n, alpha=1, beta=-1, gamma=1):
    if n <= 1:
        return alpha
    return 2 * f(n / 2) + (gamma if n % 2 else beta)

