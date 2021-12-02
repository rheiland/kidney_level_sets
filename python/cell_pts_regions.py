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
ir2 = np.where((xv > 250) & (yv > -100) & (yv < 20))

out_file = "region.dat"
fp = open(out_file, "w")
#for idx in ir1[0]:
for idx in ir2[0]:
    # print("---> ",idx)
    plt.plot(pts[idx,0],pts[idx,1],'.')
    s = "%f , %f\n" % (pts[idx,0],pts[idx,1])
    # print(s)
    fp.write(s)
plt.show()
print("\n --> ",out_file)
