import sys
import math
import matplotlib.pyplot as plt
# plt.style.use('seaborn-white')
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt

csv_file = sys.argv[1]
pts = genfromtxt(csv_file, delimiter=',')
print(pts.shape)
n = len(pts[:,0])
print("# pts = ",n)


def perp( a ):
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

def seg_intersect(a1,a2, b1,b2):
    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = perp(da)
    denom = np.dot( dap, db)
    num = np.dot( dap, dp )
    return (num / denom)*db + b1

l1_p0 = np.array( [0.0, 0.0] )
l1_p1 = np.array( [0.0, 0.0] )
l2_p0 = np.array( [0.0, 0.0] )
l2_p1 = np.array( [0.0, 0.0] )
for idx in range(n-1):
    # print(idx,") ",xpts_new[idx],ypts_new[idx], " -> ", xpts_new[idx+1],ypts_new[idx+1])
    l2_p0[0] = pts[idx,0]
    l2_p0[1] = pts[idx,1]
    l2_p1[0] = pts[idx+1,0]
    l2_p1[1] = pts[idx+1,1]

    # ptint = seg_intersect( hline0,hline1, lseg_p0,lseg_p1)
    # xmin = min(lseg_p0[0], lseg_p1[0])
    # xmax = max(lseg_p0[0], lseg_p1[0])
    # if ptint[0] >= xmin and ptint[0] <= xmax:
    #     print("--> ",ptint[0],ptint[1])
    # # else:
    #     # print("-- no intersection.")

def f(x, y):
    return np.sin(x) + np.cos(y)

nvoxels = 80
x = np.linspace(-800, 200, nvoxels)
#y = np.linspace(-600, 600, nvoxels)
y = np.linspace(0, 600, nvoxels)

X, Y = np.meshgrid(x, y)
Z = f(X, Y)   # Z.shape = (50, 50)

# for every point (voxel center) in our grid...
for iy in range(len(y)):
    yval = y[iy]
    for ix in range(len(x)):
        xval = x[ix]

        # compute distance to each bdy pt
        dist_min = 1.e6
        for idx in range(n-1):
            xd = xval - pts[idx,0]
            yd = yval - pts[idx,1]
            # dist = math.sqrt(xd*xd + yd*yd)
            dist2 = xd*xd + yd*yd
            if dist2 < dist_min:
                dist_min = dist2
        dist = math.sqrt(dist_min)
        Z[iy,ix] = dist


plt.contourf(X, Y, Z, 40, cmap='RdGy')
plt.colorbar() 
plt.title("unsigned distance to boundary")
plt.show()
