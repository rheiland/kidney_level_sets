#!/usr/bin/env python

import sys
import vtk
from numpy import genfromtxt

csv_file = sys.argv[1]
pts = genfromtxt(csv_file, delimiter=',')
print(pts.shape)
n = len(pts[:,0])
print("# pts = ",n)

tube_radius = float(sys.argv[2])

points = vtk.vtkPoints()
lines = vtk.vtkCellArray()
lines.InsertNextCell(n)
# lineSource = vtkLineSource()
# lineSource.SetPoint1(1.0, 0.0, 0.0)
# lineSource.SetPoint2(.0, 1.0, 0.0)
for idx in range(0, n):
    points.InsertPoint(idx, pts[idx,0],pts[idx,1], 0.0)
    lines.InsertCellPoint(idx)

pd = vtk.vtkPolyData()
pd.SetPoints(points)
pd.SetLines(lines)

tf = vtk.vtkTubeFilter()
# tf.SetInputData(lines)
tf.SetInputData(pd)
tf.SetRadius(20.0)
# tf.SetVaryRadiusToVaryRadiusOff()
tf.SetCapping(0)
tf.SetNumberOfSides(20)
tf.Update()

tm = vtk.vtkPolyDataMapper()
tm.SetInputData(tf.GetOutput())
tubeActor = vtk.vtkActor()
tubeActor.SetMapper(tm)
tubeActor.GetProperty().SetColor(1, 0, 0)
#ta.GetProperty().SetDiffuse(0.8)
# tubeActor.GetProperty().SetAmbient(0.25)

ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

ren.AddActor(tubeActor)
ren.SetBackground(1, 1, 1)
renWin.SetSize(800, 800)
renWin.Render()

cam1 = ren.GetActiveCamera()
# cam1.Zoom(1.5)

iren.Initialize()
renWin.Render()
iren.Start()