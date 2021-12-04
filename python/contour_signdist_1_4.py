# Compute distance from all (voxel) pts to nearest boundaries
# python contour_signdist_1_4.py region1_4_bdy.csv
_author__ = "Randy Heiland"

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

    # ptint = seg_intersect(l1_p0,l1_p1, l2_p0,l2_p1)
    # xmin = min(lseg_p0[0], lseg_p1[0])
    # xmax = max(lseg_p0[0], lseg_p1[0])
    # if ptint[0] >= xmin and ptint[0] <= xmax:
    #     print("--> ",ptint[0],ptint[1])
    # # else:
    #     # print("-- no intersection.")

def f(x, y):
    return np.sin(x) + np.cos(y)

nvoxels = 10
nvoxels = 20
nvoxels = 80
nvoxels = 50
x = np.linspace(-800, 600, nvoxels)
y = np.linspace(-600, 600, nvoxels)
y = np.linspace(-700, 700, nvoxels)

X, Y = np.meshgrid(x, y)
Z = f(X, Y)   # Z.shape = (50, 50)

l1_p0 = np.array( [0.0, 0.0] )
l1_p1 = np.array( [0.0, 0.0] )
l2_p0 = np.array( [0.0, 0.0] )
l2_p1 = np.array( [0.0, 0.0] )

intpts = []
# for every point (voxel center) in our grid...
for iy in range(len(y)):
    yval = y[iy]
    l1_p0[1] = yval
    l1_p1[1] = 800  # outside domain
    for ix in range(len(x)):
        xval = x[ix]
        l1_p0[0] = xval
        l1_p1[0] = xval

        # 1st pass: compute min distance to each bdy pt
        dist_min = 1.e6
        for idx in range(n-1):
            if math.fabs(pts[idx,0]) < 1.e-6 and math.fabs(pts[idx,1]) < 1.e-6:  # hack separator "0,0" between regions
                continue
            elif math.fabs(pts[idx+1,0]) < 1.e-6 and math.fabs(pts[idx+1,1]) < 1.e-6:  # hack separator "0,0" between regions
                continue
            xd = xval - pts[idx,0]
            yd = yval - pts[idx,1]
            dist2 = xd*xd + yd*yd
            if dist2 < dist_min:
                dist_min = dist2
            
            # how many intersections with boundaries - even or odd #?
            # l2_p0[0] = pts[idx,0]
            # l2_p0[1] = pts[idx,1]
            # l2_p1[0] = pts[idx+1,0]
            # l2_p1[1] = pts[idx+1,1]
            # ptint = seg_intersect(l1_p0,l1_p1, l2_p0,l2_p1)
            # xmin = min(lseg_p0[0], lseg_p1[0])
            # xmax = max(lseg_p0[0], lseg_p1[0])
            # if ptint[0] >= xmin and ptint[0] <= xmax:
            #     print("--> ",ptint[0],ptint[1])
            # # else:
            #     # print("-- no intersection.")

        dist = math.sqrt(dist_min)
        Z[iy,ix] = dist

        # 2nd pass: inside or outside a vessel region
        intpts.clear()
        for idx in range(n-1):
        # for idx in range(0,-1):
            if math.fabs(pts[idx,0]) < 1.e-6 and math.fabs(pts[idx,1]) < 1.e-6:  # hack separator "0,0" between regions
                continue
            elif math.fabs(pts[idx+1,0]) < 1.e-6 and math.fabs(pts[idx+1,1]) < 1.e-6:  # hack separator "0,0" between regions
                continue
            # how many intersections with boundaries - even or odd #?
            # if idx < 5:
            if True:
                # check each line seg on boundaries
                l2_p0[0] = pts[idx,0]
                l2_p0[1] = pts[idx,1]
                l2_p1[0] = pts[idx+1,0]
                l2_p1[1] = pts[idx+1,1]
                ptint = seg_intersect(l1_p0,l1_p1, l2_p0,l2_p1)
                # if ptint[0] > -800 and ptint[0] < 600 and ptint[1] > -600 and ptint[1] < 600:
                px0 = l2_p0[0]  # get left and right x values of line seg
                px1 = l2_p1[0]
                if px0 > px1:
                    px0 = l2_p1[0]
                    px1 = l2_p0[0]
                # if ptint[0] > -800 and ptint[0] < 600 and ptint[1] > -600 and ptint[1] < 600:
                # if ptint[0] >= px0 and ptint[0] <= px1 and ptint[1] > -600 and ptint[1] < 600:
                if ptint[0] >= px0 and ptint[0] <= px1 and ptint[1] > yval:
                    # print(idx,": ptint = ",ptint[0], ptint[1])
                    intpts.append(ptint[1])
        # print(iy,ix,intpts)
        if len(intpts) == 0 or len(intpts)%2 == 0:   # check for outside bdy
            # print("len(intpts)= ",len(intpts))
            Z[iy,ix] = -Z[iy,ix]
        # else:
            # print(intpts)


# plt.contourf(X, Y, Z, 40, cmap='RdGy')
plt.contourf(X, Y, Z, 40, cmap='PiYG')
# plt.contourf(X, Y, Z, 40)
plt.colorbar() 
plt.title("signed dist to bdy; grid: " + str(nvoxels) + "^2")
plt.show()
