#!/usr/bin/env python
# coding: utf-8

# Reference:
# https://towardsdatascience.com/normality-tests-in-python-31e04aa4f411
# https://stats.stackexchange.com/questions/350443/how-do-i-get-the-p-value-of-ad-test-using-the-results-of-scipy-stats-anderson
import math
import numpy as np
from scipy.stats import (
    anderson,
    shapiro,
)


def main():
    # sample dataset
    data = np.random.normal(loc=20, scale=5, size=150)
    print(data)

    '''
    Shapiro-Wilk test

    Reference:
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.shapiro.html
    '''
    print('\n> Shapiro-Wilk test')
    #stat, pvalue = shapiro(data)
    result = shapiro(data)
    print('W = %.3f, p-value = %.3f' % (result.statistic, result.pvalue))

    '''
    Anderson-Darling test

    Reference:
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.anderson.html#scipy.stats.anderson
    '''
    print('\n> Anderson-Darling test')
    result = anderson(data)
    ad_adjusted, p = calc_probability(result.statistic)
    print('A = %.3f, p-value = %.3f' % (result.statistic, p))
    print("Adjusted A^2 = ", ad_adjusted)


def calc_probability(ad):
    ad_adjusted = ad * (1 + (.75 / 50) + 2.25 / (50 ** 2))
    if ad_adjusted >= .6:
        p = math.exp(1.2937 - 5.709 * ad_adjusted - .0186 * (ad_adjusted ** 2))
    elif ad_adjusted >= .34:
        p = math.exp(.9177 - 4.279 * ad_adjusted - 1.38 * (ad_adjusted ** 2))
    elif ad_adjusted > .2:
        p = 1 - math.exp(-8.318 + 42.796 * ad_adjusted - 59.938 * (ad_adjusted ** 2))
    else:
        p = 1 - math.exp(-13.436 + 101.14 * ad_adjusted - 223.73 * (ad_adjusted ** 2))
    return ad_adjusted, p


if __name__ == '__main__':
    main()
