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
	
def vtkToNpArray(imageData):
	"""
	Convert vtk to np
	"""
	dimensions = imageData.GetDimensions()
	imageArray = vtk_to_numpy(imageData.GetPointData().GetScalars()).reshape(imageData.GetDimensions(),order='F')
	return imageArray
	
def calculateVolume(reader):
	imageArray = vtkToNpArray(reader.GetOutput())
	vol = (imageArray == 1).sum()
	vol = vol*0.4863*0.4863*4
	return vol
	
def writeCSV(names,volumes):
	with open('volumesHEI.csv', 'w', newline='') as csvfile:
		fieldnames = ['Data', 'Volume']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

		writer.writeheader()
		for i in range(0,48):
			writer.writerow({'Data': names[i], 'Volume': volumes[i]})
	
def main():
	rootDir = "D:/Data_Scans/TestAHE/InvertedN/output/predictions/testSessionDm/"
	inpDir= rootDir+"predictions"
	names=[]
	volumes=[]
	
	print("Processing >>>")
	for image in os.listdir(inpDir):
		filename = inpDir+"/"+image
		print(image)
		index=image.rindex(".nii")
		name=image[:index]
		names.append(name)
		
		#read
		reader1 = readNIFTI(filename)
		
		#calculate
		vol = calculateVolume(reader1)
		volumes.append(vol)
		
	
	writeCSV(names,volumes)
	
	
	print(vol)
	
if __name__ == '__main__':
    main()