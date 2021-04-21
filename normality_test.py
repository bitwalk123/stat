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

    scipy.stats.shapiro(x)[source]
    Perform the Shapiro-Wilk test for normality.
    The Shapiro-Wilk test tests the null hypothesis that the data was drawn
    from a normal distribution.

    Parameters
      x         : array_like
                  Array of sample data.

    Returns
      statistic : float
                  The test statistic.
      p-value   : float
                  The p-value for the hypothesis test.
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

    scipy.stats.anderson(x, dist='norm')[source]
    Anderson-Darling test for data coming from a particular distribution.
    The Anderson-Darling test tests the null hypothesis that a sample is
    drawn from a population that follows a particular distribution.
    For the Anderson-Darling test, the critical values depend on which
    distribution is being tested against. This function works for normal,
    exponential, logistic, or Gumbel (Extreme Value Type I) distributions.

    Parameters
      x                  : array_like
                           Array of sample data.
      dist               : {‘norm’, ‘expon’, ‘logistic’, ‘gumbel’,
                            ‘gumbel_l’, ‘gumbel_r’, ‘extreme1’}, optional
                           The type of distribution to test against.
                           The default is ‘norm’.
                           The names ‘extreme1’, ‘gumbel_l’ and ‘gumbel’ are
                           synonyms for the same distribution.

    Returns
      statistic          : float
                           The Anderson-Darling test statistic.
      critical_values    : list
                           The critical values for this distribution.
      significance_level : list
                           The significance levels for the corresponding
                           critical values in percents. The function
                           returns critical values for a differing set of
                           significance levels depending on the distribution
                           that is being tested against.

    Notes
    Critical values provided are for the following significance levels:

    normal/exponenential
    15%, 10%, 5%, 2.5%, 1%

    logistic
    25%, 10%, 5%, 2.5%, 1%, 0.5%

    Gumbel
    25%, 10%, 5%, 2.5%, 1%

    If the returned statistic is larger than these critical values then for
    the corresponding significance level, the null hypothesis that the data
    come from the chosen distribution can be rejected.
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
