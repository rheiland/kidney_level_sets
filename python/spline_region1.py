from scipy.interpolate import splprep, splev
import sys
from numpy import genfromtxt
import numpy as np
import matplotlib.pyplot as plt

csv_file = sys.argv[1]
pts = genfromtxt(csv_file, delimiter=',')
print(pts.shape)
n = len(pts[:,0])
print("# pts = ",n)

plt.plot(pts[:,0],pts[:,1],'.',color='k',markersize=1)

# plot grid
for xv in np.arange(-700,51,50):
    for yv in np.arange(100,600,50):
        plt.plot([-700,50],[yv,yv],'b-')
        plt.plot([xv,xv],[100,500],'b-')

# spline pts
yv = [530,400,   300,200,  150,  90, 130,  200]
xv = [-690,-660,-620,-550,-500,-340, -200,-100]
plt.plot(xv,yv,'ro')

tck, u = splprep([xv, yv], s=0)
#print("tck = ",tck)
#new_pts = splev(u, tck)
# plt.plot(new_pts[0],new_pts[1], 'g-')   # bad ~piecewise linear

unew = np.arange(0, 1.01, 0.01)
out = splev(unew, tck)
plt.plot(out[0],out[1], 'r-')

plt.show()