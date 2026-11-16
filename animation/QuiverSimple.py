"""
Modified    By    Reason
01-Jul-25   CBL   Original, matplotlib quiver example 2


References:
https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.quiver.html


"""
import matplotlib.pyplot as plt
import numpy as np

X = np.arange(-10, 10, 1)
Y = np.arange(-10, 10, 1)
U, V = np.meshgrid(X, Y)

fig, ax = plt.subplots()
q = ax.quiver(X, Y, U, V)
ax.quiverkey(q, X=0.3, Y=1.1, U=10,
             label='Quiver key, length = 10', labelpos='E')

plt.show()
