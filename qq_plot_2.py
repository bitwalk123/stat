import numpy as np
import matplotlib.pyplot as plt
import pingouin as pg

np.random.seed(123)
x = np.random.normal(size=50)
ax = pg.qqplot(x, dist='norm')
plt.show()