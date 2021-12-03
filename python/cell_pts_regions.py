# Extract 4 different regions of vessels from all of their pts
# python cell_pts_regions.py bdy_pts.dat
#
_author__ = "Randy Heiland"

import sys
from numpy import genfromtxt
import numpy as np
import matplotlib.pyplot as plt

csv_file = sys.argv[1]

pts = genfromtxt(csv_file, delimiter=',')
print(pts.shape)
#p = p1[0:9,:]
n = len(pts[:,0])
print("# pts = ",n)

xv = pts[:,0]
yv = pts[:,1]
# ir1 = np.where((xv > 200) & (yv < -150))  # keep
# ir2 = np.where((xv > 200) & (yv > -150) & (yv < 20))
#ir2 = np.where((xv > 200) & (yv > -100) & (yv < 20))

ir1 = np.where((yv > 0) & (xv < 70))
out_file = "region1.csv"

ir2 = np.where((yv > 20) & (xv > 70))
out_file = "region2.csv"

# ir2a = np.where((xv > 100) & (yv > 50) & (yv < 250))
# out_file = "region2.csv"
# ir2b = np.where((xv > 100) & (yv > 300) )
# out_file = "region2b.csv"

# ir3 = np.where((xv > 250) & (yv > -100) & (yv < 20))
# out_file = "region3.csv"
ir3 = np.where((xv > 180) & (yv < 20))
out_file = "region3.csv"

ir4 = np.where((xv < 180) & (yv < 20))
out_file = "region4.csv"

fp = open(out_file, "w")

# Which region is wanted?
#for idx in ir1[0]:
#for idx in ir2a[0]:
#for idx in ir2b[0]:
#for idx in ir1a[0]:
#for idx in ir2[0]:
#for idx in ir3[0]:
for idx in ir4[0]:
    # print("---> ",idx)
    plt.plot(pts[idx,0],pts[idx,1],'.')
    s = "%f , %f\n" % (pts[idx,0],pts[idx,1])
    # print(s)
    fp.write(s)
plt.title(out_file)
plt.show()
print("\n --> ",out_file)
