import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import sys
import math
from numpy import genfromtxt

csv_file = sys.argv[1]
pts = genfromtxt(csv_file, delimiter=',')
print(pts.shape)
#p = p1[0:9,:]
n = len(pts[:,0])
print("# pts = ",n)

train_x = pts[:,0]
train_y = pts[:,1]
 
# plt.scatter(train_x, train_y)  # markersize=0.1)
# plt.show()
 
# building polynomial model
polyModel = PolynomialFeatures(degree = 4)
# polyModel = PolynomialFeatures(degree = 7)
xpol = polyModel.fit_transform(train_x.reshape(-1, 1))
preg = polyModel.fit(xpol,train_y)

lmodel = LinearRegression(fit_intercept = True)
# lmodel = LinearRegression(fit_intercept = False)
lmodel.fit(xpol, train_y[:, np.newaxis])

# Fitting with linear model
polyfit = lmodel.predict(preg.fit_transform(train_x.reshape(-1, 1)))

# Plot results
# plt.scatter(train_x, train_y)
# plt.plot(train_x, polyfit, color = 'red')
# plt.show()
# print("train_x=",train_x)
# print("polyfit=",polyfit)

_, idx = np.unique(train_x, return_index=True)
xv = train_x[np.sort(idx)]
yv = polyfit[np.sort(idx)]

idx2 = np.argsort(xv)
xv2 = xv[idx2]
yv2 = yv[idx2]

#plt.plot(xv[:-8], yv[:-8], 'o',color = 'red')
plt.plot(xv2, yv2, '.',color = 'red')
plt.show()
lmax = 0.0
xnew = []
xnew.append(xv2[0])
ynew = []
ynew.append(yv2[0,0])
idx0 = 0
for idx in range(1,len(xv2)-1):
    dx = xv2[idx] - xv2[idx0]
    dy = yv2[idx,0] - yv2[idx0,0]
    d = math.sqrt(dx*dx + dy*dy)
    # if d > lmax:
        # lmax = d  # 7.25
    if d > 5:
        xnew.append(xv2[idx])
        ynew.append(yv2[idx,0])
        idx0 = idx
# print("x pt pairs lmax = ",lmax)
print("xnew= ",xnew)
print("ynew= ",ynew)
plt.plot(xnew,ynew,'o',color='cyan')

# print('xv=',xv)
# print('yv=',yv)
#print(np.sort(idx)])