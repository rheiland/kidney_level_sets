#
# cells_pts.py - parse an annotated .svg file containing cells of interest and extract 
#                just the Bezier pts of the cells' boundaries.
#
# Author: Randy Heiland
#
__author__ = "Randy Heiland"

import sys
import os
import xml.etree.ElementTree as ET
import math
from svg.path import parse_path, Path, Move
from scipy.spatial import ConvexHull
from scipy.special import comb
import itertools

try:
  import matplotlib
except:
  print("\n---Error: cannot import matplotlib")
  print("---Try: python -m pip install matplotlib")
  print(join_our_list)
#  print("---Consider installing Anaconda's Python 3 distribution.\n")
  raise
try:
  import numpy as np  # if mpl was installed, numpy should have been too.
except:
  print("\n---Error: cannot import numpy")
  print("---Try: python -m pip install numpy\n")
  print(join_our_list)
  raise

import matplotlib.pyplot as plt
from collections import deque
from operator import add


print("# args=",len(sys.argv)-1)
fname = "rwh1b.svg"
fname = sys.argv[1]

out_file = "bdy_pts.dat"
fp = open(out_file, "w")
#f.close()
def to_file(nx,ny):
        for idx in range(len(nx)):
            if (nx[idx] > 190) and (ny[idx] < ymax):   # 20
                s = "%f , %s\n" % (nx[idx],ny[idx])
                fp.write(s)

fig = plt.figure(figsize=(7,7))
ax = fig.gca()
#ax.set_aspect("equal")
#plt.ion()

xlist = deque()
ylist = deque()
rlist = deque()
rgb_list = deque()

print('\n---- ' + fname + ':')
tree = ET.parse(fname)
root = tree.getroot()
#  print('--- root.tag ---')
#  print(root.tag)
#  print('--- root.attrib ---')
#  print(root.attrib)

#  print('--- child.tag, child.attrib ---')
numChildren = 0
bx = [0,1,2,3]
by = [0,2,1,4]
#plt.plot(bx,by)
by2 = list(map(add,by,[1,1,1,1]))
#plt.plot(bx,by2)
#plt.show()

xoff = -300
yoff = 250
scale_factor = 5.0

msize = 1
msize = 0.5
d_thresh = 5.0
d_thresh = 10.0

ymax = -110
ymax = -150

def bernstein_poly(i, n, t):
    """
     The Bernstein polynomial of n, i as a function of t
    """

    return comb(n, i) * ( t**(n-i) ) * (1 - t)**i


def bezier_curve(points, nTimes=1000):
    """
       Given a set of control points, return the
       bezier curve defined by the control points.

       points should be a list of lists, or list of tuples
       such as [ [1,1], 
                 [2,3], 
                 [4,5], ..[Xn, Yn] ]
        nTimes is the number of time steps, defaults to 1000

        See http://processingjs.nihongoresources.com/bezierinfo/
    """

    nPoints = len(points)
    xPoints = np.array([p[0] for p in points])
    yPoints = np.array([p[1] for p in points])

    t = np.linspace(0.0, 1.0, nTimes)

    polynomial_array = np.array([ bernstein_poly(i, nPoints-1, t) for i in range(0, nPoints)   ])

    xvals = np.dot(xPoints, polynomial_array)
    yvals = np.dot(yPoints, polynomial_array)

    return xvals, yvals

def dist_endpts(nbx,nby):
    xdiff = nbx[1] - nbx[0]
    ydiff = nby[1] - nby[0]
    d = math.sqrt(xdiff*xdiff + ydiff*ydiff)
    return d

bezpts = np.random.rand(4,2)
num_eval = 6

for child in root:
#    print(child.tag, child.attrib)
    if 'data-name' in child.attrib.keys():
        print("keys = ",child.attrib.keys())
        print("data-name = ",child.attrib['data-name'])

        for child2 in child:
            # print(child2.tag)  # =  {http://www.w3.org/2000/svg}path  (or, "ellipse" at end)
            if "path" in child2.tag:
                print(child2.tag,"\n")
                d_str = child2.attrib['d']
                print("\n--- d_str = ",d_str,"\n")
                cpath = parse_path(d_str)
                print(cpath)
                xv = np.array([])
                yv = np.array([])
                # xy = np.array([],[])
                xy = np.array([[],[]], np.float64)
                for idx in range(0,len(cpath)):
                    # print("--> ",cpath[idx])
                    if 'CubicBezier' in str(cpath[idx]):
                        cbez = cpath[idx]
                        # print("--> ",cpath[idx])
                        # bx = [cbez.point(0).real, cbez.point(1).real, cbez.point(2).real, cbez.point(3).real ]
                        # by = [cbez.point(0).imag, cbez.point(1).imag, cbez.point(2).imag, cbez.point(3).imag ]
                        bx = [cbez.start.real, cbez.control1.real, cbez.control2.real, cbez.end.real ]
                        # bx = [cbez.start.real, cbez.end.real ]
                        nbx = np.array(bx)
                        # xv = np.append(xv,[cbez.start.real, cbez.control1.real, cbez.control2.real, cbez.end.real ])

                        by = [cbez.start.imag, cbez.control1.imag, cbez.control2.imag, cbez.end.imag ]
                        # by = [cbez.start.imag, cbez.end.imag ]
                        nby = np.array(by)
                        nby *= -1
                        # yv = np.append(yv,[cbez.start.imag, cbez.control1.imag, cbez.control2.imag, cbez.end.imag ])
                        # yv *= -1
                        # print("nbx= ",nbx)
                        # print("nby= ",nby)
                        nbx += xoff
                        nby += yoff
                        nbx *= scale_factor
                        nby *= scale_factor

                        if (dist_endpts(nbx,nby) < d_thresh):
                            plt.plot(nbx[0],nby[0],'.',c='black',markersize=msize)
                            plt.plot(nbx[3],nby[3],'.',c='black',markersize=msize)
                            to_file(nbx,nby)
                        else:
                            # x vals
                            bezpts[0][0] = nbx[0]
                            bezpts[1][0] = nbx[1]
                            bezpts[2][0] = nbx[2]
                            bezpts[3][0] = nbx[3]

                            # y vals
                            bezpts[0][1] = nby[0]
                            bezpts[1][1] = nby[1]
                            bezpts[2][1] = nby[2]
                            bezpts[3][1] = nby[3]
                            xv, yv= bezier_curve(bezpts, nTimes=num_eval)  # eval Bezier
                            plt.plot(xv,yv,'.',c='green',markersize=msize)
                            print("bez eval: xv= ",xv)
                            print("          yv= ",yv)

                            for idx in range(len(xv)):
                                if (xv[idx] > 190) and (yv[idx] < ymax):   # 20
                                    s = "%f , %s\n" % (xv[idx],yv[idx])
                                    fp.write(s)

                    elif 'Line' in str(cpath[idx]):
                        print("\n------ found Line(1): ",str(cpath[idx]))
                        line = cpath[idx]
                        bx = [line.start.real, line.end.real]
                        nbx = np.array(bx)
                        by = [line.start.imag, line.end.imag]
                        nby = np.array(by)
                        nby *= -1
                        nbx += xoff
                        nby += yoff
                        nbx *= scale_factor
                        nby *= scale_factor
                        plt.plot(nbx,nby,'.')
                        to_file(nbx,nby)
                    elif 'Arc' in str(cpath[idx]):
                        print("\n------ found Arc(1): ",str(cpath[idx]))
                        arc = cpath[idx]
                        bx = [arc.start.real, arc.end.real]
                        nbx = np.array(bx)
                        by = [arc.start.imag, arc.end.imag]
                        nby = np.array(by)
                        nby *= -1
                        nbx += xoff
                        nby += yoff
                        nbx *= scale_factor
                        nby *= scale_factor
                        # plt.plot(nbx,nby,'.',c='red',markersize=msize)
                        plt.plot(nbx[0],nby[0],'.',c='red',markersize=msize)
                        to_file(nbx,nby)
    elif 'id' in child.attrib.keys():
        print("keys = ",child.attrib.keys())
        print("id = ",child.attrib['id'])
        # if 'mesangium' in child.attrib['id']:
        if False:

            for child2 in child:
                # print(child2.tag)  # =  {http://www.w3.org/2000/svg}path  (or, "ellipse" at end)
                if "path" in child2.tag:
                    print(child2.tag,"\n")
                    d_str = child2.attrib['d']
                    print("\n--- d_str = ",d_str,"\n")
                    cpath = parse_path(d_str)
                    print(cpath)
                    xv = np.array([])
                    yv = np.array([])
                    # xy = np.array([],[])
                    xy = np.array([[],[]], np.float64)
                    for idx in range(0,len(cpath)):
                        # print("--> ",cpath[idx])
                        if 'CubicBezier' in str(cpath[idx]):
                            cbez = cpath[idx]
                            # print("--> ",cpath[idx])
                            # bx = [cbez.point(0).real, cbez.point(1).real, cbez.point(2).real, cbez.point(3).real ]
                            # by = [cbez.point(0).imag, cbez.point(1).imag, cbez.point(2).imag, cbez.point(3).imag ]
                            # bx = [cbez.start.real, cbez.control1.real, cbez.control2.real, cbez.end.real ]
                            bx = [cbez.start.real, cbez.end.real ]
                            nbx = np.array(bx)
                            # xv = np.append(xv,[cbez.start.real, cbez.control1.real, cbez.control2.real, cbez.end.real ])

                            # by = [cbez.start.imag, cbez.control1.imag, cbez.control2.imag, cbez.end.imag ]
                            by = [cbez.start.imag, cbez.end.imag ]
                            nby = np.array(by)
                            nby *= -1
                            # yv = np.append(yv,[cbez.start.imag, cbez.control1.imag, cbez.control2.imag, cbez.end.imag ])
                            # yv *= -1
                            # print("nbx= ",nbx)
                            # print("nby= ",nby)
                            nbx += xoff
                            nby += yoff
                            if (dist_endpts(nbx,nby) < d_thresh):
                                plt.plot(nbx,nby,'.',c='green',markersize=msize)
                                to_file(nbx,nby)
                        elif 'Line' in str(cpath[idx]):
                            print("\n------ found Line(2): ",str(cpath[idx]))
                            line = cpath[idx]
                            bx = [line.start.real, line.end.real]
                            nbx = np.array(bx)
                            by = [line.start.imag, line.end.imag]
                            nby = np.array(by)
                            nby *= -1
                            nbx += xoff
                            nby += yoff
                            plt.plot(nbx,nby,'.',c='cyan',markersize=msize)
                            to_file(nbx,nby)
                        elif 'Arc' in str(cpath[idx]):
                            print("\n------ found Arc(2): ",str(cpath[idx]))
                            arc = cpath[idx]
                            bx = [arc.start.real, arc.end.real]
                            nbx = np.array(bx)
                            by = [arc.start.imag, arc.end.imag]
                            nby = np.array(by)
                            nby *= -1
                            nbx += xoff
                            nby += yoff
                            plt.plot(nbx,nby,'.',c='yellow',markersize=msize)
                            to_file(nbx,nby)

plt.show()

print("\n--> ",out_file)