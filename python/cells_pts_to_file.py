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

fp = open("bdy_pts.dat", "w")
#f.close()
def to_file(nx,ny):
    if (nx[0] > 190) and (ny[0] < 20):
        for idx in range(len(nx)):
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
                        print("--> ",cpath[idx])
                        # bx = [cbez.point(0).real, cbez.point(1).real, cbez.point(2).real, cbez.point(3).real ]
                        # by = [cbez.point(0).imag, cbez.point(1).imag, cbez.point(2).imag, cbez.point(3).imag ]
                        bx = [cbez.start.real, cbez.control1.real, cbez.control2.real, cbez.end.real ]
                        nbx = np.array(bx)
                        # xv = np.append(xv,[cbez.start.real, cbez.control1.real, cbez.control2.real, cbez.end.real ])
                        by = [cbez.start.imag, cbez.control1.imag, cbez.control2.imag, cbez.end.imag ]
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
                        plt.plot(nbx,nby,'.',c='black',markersize=msize)
                        to_file(nbx,nby)
                    elif 'Line' in str(cpath[idx]):
                        print("\n------ found: ",str(cpath[idx]))
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
                        print("\n------ found: ",str(cpath[idx]))
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
                        plt.plot(nbx,nby,'.',c='red',markersize=msize)
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
                            print("--> ",cpath[idx])
                            # bx = [cbez.point(0).real, cbez.point(1).real, cbez.point(2).real, cbez.point(3).real ]
                            # by = [cbez.point(0).imag, cbez.point(1).imag, cbez.point(2).imag, cbez.point(3).imag ]
                            bx = [cbez.start.real, cbez.control1.real, cbez.control2.real, cbez.end.real ]
                            nbx = np.array(bx)
                            # xv = np.append(xv,[cbez.start.real, cbez.control1.real, cbez.control2.real, cbez.end.real ])
                            by = [cbez.start.imag, cbez.control1.imag, cbez.control2.imag, cbez.end.imag ]
                            nby = np.array(by)
                            nby *= -1
                            # yv = np.append(yv,[cbez.start.imag, cbez.control1.imag, cbez.control2.imag, cbez.end.imag ])
                            # yv *= -1
                            # print("nbx= ",nbx)
                            # print("nby= ",nby)
                            nbx += xoff
                            nby += yoff
                            plt.plot(nbx,nby,'.',c='green',markersize=msize)
                        elif 'Line' in str(cpath[idx]):
                            print("\n------ found: ",str(cpath[idx]))
                            line = cpath[idx]
                            bx = [line.start.real, line.end.real]
                            nbx = np.array(bx)
                            by = [line.start.imag, line.end.imag]
                            nby = np.array(by)
                            nby *= -1
                            nbx += xoff
                            nby += yoff
                            plt.plot(nbx,nby,'.',c='cyan',markersize=msize)
                        elif 'Arc' in str(cpath[idx]):
                            print("\n------ found: ",str(cpath[idx]))
                            arc = cpath[idx]
                            bx = [arc.start.real, arc.end.real]
                            nbx = np.array(bx)
                            by = [arc.start.imag, arc.end.imag]
                            nby = np.array(by)
                            nby *= -1
                            nbx += xoff
                            nby += yoff
                            plt.plot(nbx,nby,'.',c='yellow',markersize=msize)

plt.show()