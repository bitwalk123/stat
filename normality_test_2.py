#!/usr/bin/env python
# coding: utf-8

# Reference:
# https://towardsdatascience.com/normality-tests-in-python-31e04aa4f411
import csv
import math
import numpy as np
from scipy.stats import (
    anderson,
    shapiro,
)


# Reference
# https://stats.stackexchange.com/questions/350443/how-do-i-get-the-p-value-of-ad-test-using-the-results-of-scipy-stats-anderson
def calc_probability(ad, n):
    ad_adj = ad * (1 + (0.75 / n) + 2.25 / (n ** 2))
    if ad_adj >= 0.6:
        prob = math.exp(1.2937 - 5.709 * ad_adj - 0.0186 * (ad_adj ** 2))
    elif ad_adj >= 0.34:
        prob = math.exp(0.9177 - 4.279 * ad_adj - 1.38 * (ad_adj ** 2))
    elif ad_adj > 0.2:
        prob = 1 - math.exp(-8.318 + 42.796 * ad_adj - 59.938 * (ad_adj ** 2))
    else:
        prob = 1 - math.exp(-13.436 + 101.14 * ad_adj - 223.73 * (ad_adj ** 2))
    return prob


def main():
    # sample dataset
    filename = 'data_norm.csv'
    file = open(filename)
    reader = csv.reader(file)
    next(reader)  # skip first row
    data = []
    for row in reader:
        data.append(float(row[0]))
    data = np.array(data)

    '''
    Shapiro-Wilk test

    Reference:
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.shapiro.html
    '''
    print('\n> Shapiro-Wilk test')
    result_shapiro = shapiro(data)
    print('W = %.5f, p-value = %.4f' % (result_shapiro.statistic, result_shapiro.pvalue))

    '''
    Anderson-Darling test

    Reference:
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.anderson.html#scipy.stats.anderson
    '''
    print('\n> Anderson-Darling test')
    result_anderson = anderson(data)
    pvalue = calc_probability(result_anderson.statistic, data.size)
    print('A = %.5f, p-value = %.4f' % (result_anderson.statistic, pvalue))


if __name__ == '__main__':
    main()
