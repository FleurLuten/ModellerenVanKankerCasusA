import pandas as pd
from matplotlib import pyplot as plt

ts = [0, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 17, 18, 19, 20, 21]
Vs = [41.8, 85, 114, 162.3, 178.3, 325, 623.7, 648.4, 835.9, 1030.4, 1141.8, 1499.9, 1429.3, 1609.3, 1678.3, 1564]

pd.DataFrame({'$t$': ts, '$V$': Vs}).T

plt.axhline(0.0, color='k'); plt.axvline(0.0, color='k')
plt.plot(ts, Vs, 'or')
plt.title('Tumor volume growth'); plt.xlabel('$t$ (days)'); plt.ylabel('$V(t)$ (mm³)')
plt.grid(True); plt.box(False)
plt.show()