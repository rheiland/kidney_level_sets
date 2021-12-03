# fit a B-spline to region3 pts
# python spline_region3.py region3.csv
_author__ = "Randy Heiland"

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
for xv in np.arange(175,451,25):
    for yv in np.arange(25,-275,-25):
        plt.plot([175,450],[yv,yv],'b-',linewidth=1)
        plt.plot([xv,xv],[25,-250],'b-',linewidth=1)

# spline pts
yv = [-230,-220, -175,-150,-75, -25, 0,  0, -20,-75,-125,-175,-205,-225,-230]
xv = [300,  260,  210, 200,210, 250,300,350,400,435,440, 425,400,350,300]
plt.plot(xv,yv,'ro')

tck, u = splprep([xv, yv], s=0)
#print("tck = ",tck)
#new_pts = splev(u, tck)
# plt.plot(new_pts[0],new_pts[1], 'g-')   # bad ~piecewise linear

#unew = np.arange(0, 1.01, 0.01)
unew = np.arange(0, 1.01, 0.02)
out = splev(unew, tck)
plt.plot(out[0],out[1], 'r-')
print("out[0]= ",out[0])

out_file = "region3_bdy.csv"
fp = open(out_file, "w")
for idx in range(len(out[0])):
    s = "%f , %f\n" % (out[0][idx],out[1][idx])
    fp.write(s)
print("--> ",out_file)

plt.title(csv_file)
plt.show()