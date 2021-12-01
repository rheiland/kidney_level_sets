import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import sys
from numpy import genfromtxt

csv_file = sys.argv[1]
pts = genfromtxt(csv_file, delimiter=',')
print(pts.shape)
#p = p1[0:9,:]
n = len(pts[:,0])
print("# pts = ",n)

train_x = pts[:,0]
train_y = pts[:,1]
 
plt.scatter(train_x, train_y)
# plt.show()
 
# building polynomial model
polyModel = PolynomialFeatures(degree = 4)
# polyModel = PolynomialFeatures(degree = 7)
xpol = polyModel.fit_transform(train_x.reshape(-1, 1))
preg = polyModel.fit(xpol,train_y)

# lmodel = LinearRegression(fit_intercept = True)
lmodel = LinearRegression(fit_intercept = False)
lmodel.fit(xpol, train_y[:, np.newaxis])

# Fitting with linear model
polyfit = lmodel.predict(preg.fit_transform(train_x.reshape(-1, 1)))

# Plot results
# plt.scatter(train_x, train_y)
plt.plot(train_x, polyfit, color = 'red')
plt.show()
# print(polyfit)
