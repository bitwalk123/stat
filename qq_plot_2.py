import numpy as np
import matplotlib.pyplot as plt
import pingouin as pg

# sample dataset
filename = 'data_norm.csv'
data = np.loadtxt(filename, skiprows=1)

ax = pg.qqplot(data, dist='norm')
ax.set_title('example of Q-Q plot')

plt.show()
