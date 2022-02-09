# fit a B-spline to points on a glom vessel

import sys
from scipy.interpolate import splprep, splev
from numpy import genfromtxt
import numpy as np
import matplotlib.pyplot as plt

# csv_file = sys.argv[1]
# pts = genfromtxt(csv_file, delimiter=',')
# print(pts.shape)
# n = len(pts[:,0])
# print("# pts = ",n)

# plt.plot(pts[:,0],pts[:,1],'.',color='k',markersize=1)

# plot grid
xmin,xmax,xdel = -400,400,50
ymin,ymax,ydel = -400,400,50
for xv in np.arange(xmin,xmax,xdel):
    for yv in np.arange(ymin,ymax,ydel):
        plt.plot([xmin,xmax],[yv,yv],'b-',linewidth=1)
        plt.plot([xv,xv],[ymin,ymax],'b-',linewidth=1)

xv = [-300, -250,-200, -100, -50,  0,  75,  150, 175, 150, 75, 10, 0]
print(xv)
y0 = 75
yv=  [ y0,  y0, y0,  y0, 110, 150, 170, 150, 100, 50, 50,  25, 0]
print(yv)
xv2=xv.copy()
xv2.reverse()
print("xv2[1:] = ",xv2[1:])
xv += xv2[1:]
yv2 = [y * -1 for y in yv]
yv2.reverse()
yv += yv2[1:]
print(xv)
print(yv)
plt.plot(xv,yv,'ro')

tck, u = splprep([xv, yv], s=0)
#print("tck = ",tck)
#new_pts = splev(u, tck)
# plt.plot(new_pts[0],new_pts[1], 'g-')   # bad ~piecewise linear

unew = np.arange(0, 1.01, 0.01)
out = splev(unew, tck)
plt.plot(out[0],out[1], 'r-')
print(out[0])

out_file = "glom_vessel.csv"
fp = open(out_file, "w")
for idx in range(len(out[0])):
    s = "%f , %f\n" % (out[0][idx],out[1][idx])
    fp.write(s)
print("--> ",out_file)

# plt.title(csv_file)

plt.show()