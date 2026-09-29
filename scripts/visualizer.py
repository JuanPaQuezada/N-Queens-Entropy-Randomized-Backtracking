import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
dx, dy=0.015, 0.05
P=np.arange(-0.5,5.0,dx)
Q=np.arange(-0.5,5.0,dy)
X,Y=np.meshgrid(P,Q)

min_max=np.min(P), np.max(P),np.min(Q),np.max(Q)
res=np.add.outer(range(8),range(8))%2
plt.imshow(res,cmap="binary_r")
plt.xticks([])
plt.yticks([])
plt.title("Tablero de ajedrez")
plt.show()
