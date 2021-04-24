from scipy import stats
import matplotlib.pyplot as plt
import numpy as np

# sample dataset
filename = 'data_norm.csv'
data = np.loadtxt(filename, skiprows=1)

fig = plt.figure()
ax = fig.add_subplot(111)
res = stats.probplot(data, plot=plt)
ax.set_title('example of Q-Q plot')

plt.show()
