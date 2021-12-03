import matplotlib.pyplot as plt
plt.style.use('seaborn-white')
import numpy as np

def f(x, y):
#    return np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)
    return np.sin(x) + np.cos(y)

x = np.linspace(-700, 200, 10)
y = np.linspace(-550, 550, 10)

X, Y = np.meshgrid(x, y)
Z = f(X, Y)
#plt.contour(X, Y, Z, colors='black');
plt.contour(X, Y, Z, 20, cmap='RdGy');
plt.show()
