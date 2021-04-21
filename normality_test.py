#!/usr/bin/env python
# coding: utf-8

# Reference:
# https://towardsdatascience.com/normality-tests-in-python-31e04aa4f411
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
    stat, pvalue = shapiro(data)
    print('stat = %.3f, p-value = %.3f' % (stat, pvalue))

    if pvalue > 0.05:
        # If the p-value > 0.05, then we fail to reject the null hypothesis
        # i.e. we assume the distribution of our variable is normal/gaussian.
        print('Probably Gaussian at 5% level of significance')
    else:
        # If the p-value ≤ 0.05, then we reject the null hypothesis
        # i.e. we assume the distribution of our variable is not normal/gaussian.
        print('Probably not Gaussian at 5% level of significance')

    '''
    Shapiro-Wilk test

    Reference:
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.anderson.html#scipy.stats.anderson
    '''
    print('\n> Anderson-Darling test')
    result = anderson(data)
    print('stat = %.3f' % (result.statistic))
    for i in range(len(result.critical_values)):
        sig_lev, crit_val = result.significance_level[i], result.critical_values[i]
        if result.statistic < crit_val:
            print('Probably Gaussian : %.3f critical at %2d%% level of significance' % (crit_val, sig_lev))
        else:
            print('Probably not Gaussian : %.3f critical at %2d%% level of significance' % (crit_val, sig_lev))


if __name__ == '__main__':
    main()
