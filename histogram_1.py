import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# sample dataset
filename = 'data_norm.csv'
data = np.loadtxt(filename, skiprows=1)

sns.set_style('darkgrid')
sns.histplot(data, kde=True)
plt.show()