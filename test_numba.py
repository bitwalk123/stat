#!/usr/bin/env python
# coding: utf-8
from numba import jit
import random
import time


def benchmark(f):
    def wrap(*args, **kwargs):
        time_start = time.time()
        ret = f(*args, **kwargs)
        time_end = time.time()
        msec_elapsed = (time_end - time_start) * 1000.
        print('{:s} function tool {:.3f} ms'.format(f.__name__, msec_elapsed))
        return ret

    return wrap


@benchmark
def monte_carlo_pi_1(nsamples):
    acc = 0
    for i in range(nsamples):
        x = random.random()
        y = random.random()
        if (x ** 2 + y ** 2) < 1.0:
            acc += 1
    return 4.0 * acc / nsamples


@benchmark
@jit(nopython=True)
def monte_carlo_pi_2(nsamples):
    acc = 0
    for i in range(nsamples):
        x = random.random()
        y = random.random()
        if (x ** 2 + y ** 2) < 1.0:
            acc += 1
    return 4.0 * acc / nsamples


def main():
    n = 10000000
    ans1 = monte_carlo_pi_1(n)
    print('Pi =', ans1)
    ans2 = monte_carlo_pi_2(n)
    print('Pi =', ans2)


if __name__ == '__main__':
    main()
