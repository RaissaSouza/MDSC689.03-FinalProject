import itk
import vtk
import numpy as np
import sys
import argparse
from vtk.util.numpy_support import vtk_to_numpy, numpy_to_vtk
import tkinter
import tkinter.filedialog 
import os
import matplotlib.pyplot as plt
import SimpleITK as sitk
import csv


def readNIFTI(filename):
	"""
	Read NIFTI object
	"""
	reader = vtk.vtkNIFTIImageReader()
	reader.SetFileName(filename)
	reader.Update()
	return reader
	
def marchingCubes(image):
	"""
	Extract surface with Marching cubes 
	"""
	mc = vtk.vtkMarchingCubes()
	mc.SetInputData(image)
	mc.ComputeNormalsOn()
	mc.ComputeGradientsOn()
	mc.SetValue(0, 1)
	mc.Update()
	
	# To remain largest region
	confilter =vtk.vtkPolyDataConnectivityFilter()
	confilter.SetInputData(mc.GetOutput())
	confilter.SetExtractionModeToLargestRegion()
	confilter.Update()
	return confilter.GetOutput()
	
def main():

	#Show your nice GUI to get the input file
	root = tkinter.Tk()
	root.withdraw()
	imagefile1 = tkinter.filedialog.askopenfilename()

	#extract the file extension
	ext1 = os.path.splitext(imagefile1)[1]
	root.destroy()
	
	image = readNIFTI(imagefile1)
	#Marching Cubes
	resMc=marchingCubes(image.GetOutput())
	
	#surface mapper
	mapper = vtk.vtkPolyDataMapper()
	mapper.SetInputData(resMc)
	mapper.SetScalarVisibility(0)
	mapper.SetScalarRange(image.GetOutput().GetScalarRange())
	mapper.Update()
	
	#surface actor
	actorMc = vtk.vtkActor()
	actorMc.SetMapper(mapper)
	actorMc.GetProperty().SetColor(1,0,1)
	actorMc.GetProperty().SetOpacity(1.0)
	
	#display
	renderer = vtk.vtkRenderer()
	renWin = vtk.vtkRenderWindow()
	
	renderer.AddActor(actorMc)
	renWin.AddRenderer(renderer)
	renWin.SetSize(1024,720)
	
	iren = vtk.vtkRenderWindowInteractor()
	iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
	
	iren.SetRenderWindow(renWin)
	iren.Initialize()
	iren.Start()
	
if __name__ == '__main__':
    main()