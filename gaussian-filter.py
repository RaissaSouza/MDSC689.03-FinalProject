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


def main():
	
	
	rootDir = "D:/Data_Scans/"
	outDir1 = "D:/Data_Scans/Scans_4/"
	inpDir= rootDir+"Scans_T"
	
	print("Processing >>>")
	for image in os.listdir(inpDir):
		filename = inpDir+"/"+image
		print(image)
		#read
		inputImage = sitk.ReadImage(filename)
		index=image.rindex(".nii")
		name=image[:index]

		
		gaussian11 = sitk.DiscreteGaussianImageFilter()
		#gaussian11.SetVariance(4.0)
		img = gaussian11.Execute(inputImage)
		
				
		#write new images
		dst_path1=outDir1+name+"G.nii"
		
		sitk.WriteImage(img, dst_path1)
		
		
		
		
	
		
	
	
	
if __name__ == '__main__':
    main()