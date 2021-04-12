
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

reader1 = vtk.vtkNIFTIImageReader()
actor1 = vtk.vtkActor2D()
renderer1 = vtk.vtkRenderer()


reader2 = vtk.vtkNIFTIImageReader()
actor2 = vtk.vtkActor2D()
renderer2 = vtk.vtkRenderer()

renWin1 = vtk.vtkRenderWindow()

def addCaption(msg):
	"""
	Add a message on the top left of the screen describing how to use the keys and mouse to interact with the object
	"""
	usageTextProp = vtk.vtkTextProperty()
	usageTextProp.SetFontFamilyToCourier()
	usageTextProp.SetFontSize(18)
	usageTextProp.SetVerticalJustificationToTop()
	usageTextProp.SetJustificationToLeft()
	usageTextProp.SetColor(1,0,0)
	usageTextProp.BoldOn()

 
	usageTextMapper = vtk.vtkTextMapper()
	usageTextMapper.SetInput(msg)
	usageTextMapper.SetTextProperty(usageTextProp)

	usageTextActor = vtk.vtkActor2D()
	usageTextActor.SetMapper(usageTextMapper)
	usageTextActor.SetPosition(250, 50)
	

	return usageTextActor

def readNIFTI(filename):
	"""
	Read NIFTI object
	"""
	reader = vtk.vtkNIFTIImageReader()
	reader.SetFileName(filename)
	reader.Update()
	return reader
	
def loadSlices(reader1, reader2):
	
	
	#original slices mapper
	mapper1 = vtk.vtkImageMapper()
	mapper1.SetInputData(reader1.GetOutput())
	mapper1.SetZSlice(17)
	mapper1.SetColorWindow(5)
	mapper1.SetColorLevel(1)
	
	#original actor
	global actor1
	actor1.SetMapper(mapper1)
	
	
	# processed image mapper
	mapper2 = vtk.vtkImageMapper()
	mapper2.SetInputData(reader2.GetOutput())
	mapper2.SetZSlice(17)
	mapper2.SetColorWindow(5)
	mapper2.SetColorLevel(1)
	
	#reslice actor
	global actor2
	actor2.SetMapper(mapper2)
	
	global renderer1
	global renderer2
	
	leftViewport = [0.0, 0.0, 0.5, 1.0];
	rightViewport = [0.5, 0.0, 1.0, 1.0];
	
	renderer1.AddActor2D(actor1)
	renderer1.AddActor2D(addCaption("a"))
	renderer1.SetViewport(leftViewport)
	
	renderer2.AddActor2D(actor2)
	renderer2.AddActor2D(addCaption("b"))
	renderer2.SetViewport(rightViewport)
	
	global renWin1
	renWin1.AddRenderer(renderer1)
	renWin1.AddRenderer(renderer2)
	renWin1.SetSize(1024,720)
	
def main():
	
	#Show your nice GUI to get the input file
	root = tkinter.Tk()
	root.withdraw()
	imagefile1 = tkinter.filedialog.askopenfilename()

	#extract the file extension
	ext1 = os.path.splitext(imagefile1)[1]
	root.destroy()
	
	#Show your nice GUI to get the input file
	root2 = tkinter.Tk()
	root2.withdraw()
	imagefile2 = tkinter.filedialog.askopenfilename()

	#extract the file extension
	ext2 = os.path.splitext(imagefile2)[1]
	root2.destroy()
	
	
	global reader1
	global reader2
	
	
	reader1 = readNIFTI(imagefile1)
	reader2 = readNIFTI(imagefile2)
	
	loadSlices(reader1,reader2)
	
	global renWin1
		
	#interactor1
	iren1 = vtk.vtkRenderWindowInteractor()
	iren1.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
	
	iren1.SetRenderWindow(renWin1)
	iren1.Initialize()
	iren1.Start()
	
	
if __name__ == '__main__':
    main()