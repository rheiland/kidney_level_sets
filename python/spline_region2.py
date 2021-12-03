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
for xv in np.arange(0,500,25):
    for yv in np.arange(100,450,25):
        plt.plot([0,500],[yv,yv],'b-',linewidth=1)
        plt.plot([xv,xv],[100,450],'b-',linewidth=1)

# spline pts
yv = [210,300, 350, 380, 400, 405, 375, 325, 300, 270, 235, 205, 185,150,150,150,155,175,210]
xv = [90, 100, 130, 175, 250, 325, 400, 460, 480, 460, 400, 325, 285,270,250,225,175,125,90]
plt.plot(xv,yv,'ro')

tck, u = splprep([xv, yv], s=0)
#print("tck = ",tck)
#new_pts = splev(u, tck)
# plt.plot(new_pts[0],new_pts[1], 'g-')   # bad ~piecewise linear

unew = np.arange(0, 1.01, 0.01)
out = splev(unew, tck)
plt.plot(out[0],out[1], 'r-')
print("out[0]= ",out[0])

out_file = "region2_bdy.csv"
fp = open(out_file, "w")
for idx in range(len(out[0])):
    s = "%f , %f\n" % (out[0][idx],out[1][idx])
    fp.write(s)
print("--> ",out_file)

plt.title(csv_file)
plt.show()