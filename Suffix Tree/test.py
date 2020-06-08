import matplotlib.pyplot as plt
import numpy as np

xlabel = np.array(['Brute force', 'Binary search', 'LCP'])
y = np.array([65.97, 0.68, 1.97])
x = np.arange(len(y))

# plt.barh(y_pos, performance, xerr=error, alpha=0.4)

plt.figure(0)
plt.barh(x, y)
plt.yticks(x, xlabel)
plt.show()
