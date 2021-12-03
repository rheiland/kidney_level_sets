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
        plt.plot([-700,50],[yv,yv],'b-',linewidth=1)
        plt.plot([xv,xv],[100,550],'b-',linewidth=1)

# spline pts
yv = [530,400,   300,200,  150,  90, 130,  200, 300, 400,500,525,450,350, 300, 200,150,170,250,350,450,530]
xv = [-690,-660,-620,-550,-500,-340, -200,-100, -10, 50, 20, -50,-210,-235,-220,-225, -325,-400,-510,-570,-605,-620]
plt.plot(xv,yv,'ro')

tck, u = splprep([xv, yv], s=0)
#print("tck = ",tck)
#new_pts = splev(u, tck)
# plt.plot(new_pts[0],new_pts[1], 'g-')   # bad ~piecewise linear

unew = np.arange(0, 1.01, 0.01)
out = splev(unew, tck)
plt.plot(out[0],out[1], 'r-')
print("out[0]= ",out[0])

out_file = "region1_bdy.csv"
fp = open(out_file, "w")
for idx in range(len(out[0])):
    s = "%f , %f\n" % (out[0][idx],out[1][idx])
    fp.write(s)
print("--> ",out_file)

plt.title(csv_file)
plt.show()