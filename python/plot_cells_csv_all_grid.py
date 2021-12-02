import sys
from numpy import genfromtxt
import numpy as np
import matplotlib.pyplot as plt

csv_file = sys.argv[1]

# cell = genfromtxt('cells_5um.csv', delimiter=',')
# cell = genfromtxt('glom_cells.csv', delimiter=',')
# cell = genfromtxt('ftu_cells.csv', delimiter=',')
cell = genfromtxt(csv_file, delimiter=',')
print(cell.shape)
#p = p1[0:9,:]
n = len(cell[:,0])
print("# cells = ",n)
#plt.plot(cell[:,0],p1[:,1],'r.')
xmin=80
xmax=290
ymin=-200
ymax=0
# for idx in range(n):
#     if cell[idx,0]>xmin and cell[idx,0]<xmax and cell[idx,1]>ymin and cell[idx,1]<ymax and cell[idx,3]==5 and cell[idx,4]==7:
#         plt.plot(cell[idx,0],cell[idx,1],'r.')
#         if cell[idx,0]>150 and cell[idx,0]<160 and cell[idx,1]>-100 and cell[idx,1]<-75:
#             print(idx,cell[idx,:])
nmin=20
nmax=45

# plt.plot(cell[:,0],cell[:,1],'.')

for xv in np.arange(-700,51,50):
    for yv in np.arange(100,600,50):
        plt.plot([-700,50],[yv,yv],'b-')
        plt.plot([xv,xv],[100,500],'b-')

# for region (blob) #1
xv1 = -660
xv2 = -550
yv1 = 520
yv2 = 250
plt.plot([xv1,xv2],[yv1,yv2],'r-')
xv3 = -400
yv3 = 125
xv3 = -500
yv3 = 200
plt.plot([xv2,xv3],[yv2,yv3],'r-')
xv4 = -300
yv4 = 110
plt.plot([xv3,xv4],[yv3,yv4],'r-')
# xv5 = -50
# yv5 = 500
xv5 = 50
yv5 = 450
plt.plot([xv4,xv5],[yv4,yv5],'r-')

def left_of_line(xa,ya, xb,yb, xp,yp):  
     return ((xb - xa)*(yp - ya) - (yb - ya)*(xp - xa)) > 0

for idx in range(len(cell[:,0])):
    # if left_of_line(xv1,yv1, xv2,yv2, cell[idx,0],cell[idx,1]):
    #     plt.plot(cell[idx,0],cell[idx,1],'r.')
    # else:
    #     plt.plot(cell[idx,0],cell[idx,1],'g.')

    if left_of_line(xv4,yv4, xv5,yv5, cell[idx,0],cell[idx,1]):
        # plt.plot(cell[idx,0],cell[idx,1],'r.')
        pass
    else:
        plt.plot(cell[idx,0],cell[idx,1],'g.')

for idx in range(len(cell[:,0])):
    if left_of_line(xv4,yv4, xv3,yv3, cell[idx,0],cell[idx,1]):
        plt.plot(cell[idx,0],cell[idx,1],'g.')

for idx in range(len(cell[:,0])):
    if left_of_line(xv2,yv2, xv1,yv1, cell[idx,0],cell[idx,1]):
        plt.plot(cell[idx,0],cell[idx,1],'g.')
plt.show()
