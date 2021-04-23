import numpy as np
import matplotlib.pyplot as plt
import pingouin as pg

x = np.random.normal(size=100)
ax = pg.qqplot(x, dist='norm')
plt.show()
