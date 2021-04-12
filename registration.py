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
	
def colorMap(segmentedImage):
	#lookup table	
	lookupTable = vtk.vtkLookupTable()
	lookupTable.SetNumberOfTableValues(2)
	lookupTable.SetRange(0,1)
	lookupTable.SetTableValue(0, 0.0, 0.0, 0.0, 0.0) # black,transparent
	lookupTable.SetTableValue(1, 1.0, 0.0, 1.0, 1.0) # green, opaque
	lookupTable.Build()
	
	#maptoColour
	mapToColors=vtk.vtkImageMapToColors()
	mapToColors.SetLookupTable(lookupTable)
	mapToColors.PassAlphaToOutputOn()
	mapToColors.SetInputData(segmentedImage.GetOutput())
	
	return mapToColors
	
def main():

	#Show your nice GUI to get the input file
	root = tkinter.Tk()
	root.withdraw()
	imagefile1 = tkinter.filedialog.askopenfilename()

	#extract the file extension
	ext1 = os.path.splitext(imagefile1)[1]
	root.destroy()
	
	#Show your nice GUI to get the input file
	root = tkinter.Tk()
	root.withdraw()
	imagefile2 = tkinter.filedialog.askopenfilename()

	#extract the file extension
	ext2 = os.path.splitext(imagefile2)[1]
	root.destroy()
	
	image = readNIFTI(imagefile1)
	segmentedImage = readNIFTI(imagefile2)
	
	#mapper
	mapper = vtk.vtkImageMapper()
	mapper.SetInputData(image.GetOutput())
	mapper.SetZSlice(27)
	mapper.SetColorWindow(9)
	mapper.SetColorLevel(4)
	
	mapperSeg = vtk.vtkImageMapper()
	imageMapped = colorMap(segmentedImage)
	mapperSeg.SetInputConnection(imageMapped.GetOutputPort())
	mapperSeg.SetZSlice(27)
	mapperSeg.SetColorWindow(1)
	mapperSeg.SetColorLevel(0)
	
	#actor
	actorImage = vtk.vtkActor2D()
	actorImage.SetMapper(mapper)
	
	actorMap = vtk.vtkActor2D()
	actorMap.SetMapper(mapperSeg)
	
	#display
	renderer = vtk.vtkRenderer()
	renWin = vtk.vtkRenderWindow()
	
	renderer.AddActor2D(actorImage)
	renderer.AddActor2D(actorMap)
	renWin.AddRenderer(renderer)
	renWin.SetSize(1024,720)
	
	iren = vtk.vtkRenderWindowInteractor()
	iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
	
	iren.SetRenderWindow(renWin)
	iren.Initialize()
	iren.Start()
	
if __name__ == '__main__':
    main()
	
