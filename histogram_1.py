import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

d = np.random.normal(size=50)

sns.set_style('darkgrid')
sns.histplot(d, kde=True)
plt.show()