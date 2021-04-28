#!/usr/bin/env python
# coding: utf-8
import csv
import math
import numpy as np
import matplotlib.pyplot as plt
import pingouin as pg
import seaborn as sns
from scipy.stats import (
    anderson,
    shapiro,
)

'''
Reference
https://stats.stackexchange.com/questions/350443/how-do-i-get-the-p-value-of-ad-test-using-the-results-of-scipy-stats-anderson
'''


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
    data = np.loadtxt(filename, skiprows=1)
    print(data)

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

    sns.set_theme(style="whitegrid")
    fig = plt.figure(figsize=(5, 10))
    gs = fig.add_gridspec(12, 1)

    ax1 = fig.add_subplot(gs[0:5, 0])
    ax2 = fig.add_subplot(gs[6:7, 0])
    ax3 = fig.add_subplot(gs[8:11, 0])

    # Q-Q plot
    a = pg.qqplot(data, dist='norm', ax=ax1)
    a.set_title('Probability Plot')

    # Boxplot
    b = sns.boxplot(x=data, ax=ax2)

    # Histogram
    c = sns.histplot(data, kde=True, ax=ax3)
    c.set_title('Histogram')

    plt.show()


if __name__ == '__main__':
    main()
