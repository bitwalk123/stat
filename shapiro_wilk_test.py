#!/usr/bin/env python
# coding: utf-8
# Reference:
# https://towardsdatascience.com/normality-tests-in-python-31e04aa4f411
import numpy as np
from scipy.stats import shapiro

data = np.random.normal(loc=20, scale=5, size=150)
print(data)

# Reference:
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.shapiro.html
#
# scipy.stats.shapiro(x)[source]
# Perform the Shapiro-Wilk test for normality.
# The Shapiro-Wilk test tests the null hypothesis that the data was drawn from
# a normal distribution.
#
# Parameters
#   x         : array_like
#               Array of sample data.
#
# Returns
#   statistic : float
#               The test statistic.
#   p-value   : float
#               The p-value for the hypothesis test.
stat, pvalue = shapiro(data)
print('\nShapiro-Wilk test')
print('stat = %.3f, p = %.3f' % (stat, pvalue))

if pvalue > 0.05:
    # If the p-value > 0.05, then we fail to reject the null hypothesis
    # i.e. we assume the distribution of our variable is normal/gaussian.
    print('Probably Gaussian')
else:
    # If the p-value ≤ 0.05, then we reject the null hypothesis
    # i.e. we assume the distribution of our variable is not normal/gaussian.
    print('Probably not Gaussian')
