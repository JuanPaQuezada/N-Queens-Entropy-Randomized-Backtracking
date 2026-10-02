import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

def plot_board(queens, n):
    dx, dy=0.015, 0.05
    P=np.arange(-0.5,5.0,dx)
    Q=np.arange(-0.5,5.0,dy)
    X,Y=np.meshgrid(P,Q)

    min_max=np.min(P), np.max(P),np.min(Q),np.max(Q)
    res=np.add.outer(range(n),range(n))%2
    plt.imshow(res,cmap="binary_r")
    xcoords=[q[0] for q in queens]
    ycoords=[q[1] for q in queens]
    plt.scatter(xcoords,ycoords,c="red",s=100,zorder=5)
    plt.xticks([])
    plt.yticks([])
    plt.title("Tablero de ajedrez")
    plt.show()
