#import itk
#import vtk
#import numpy as np
#import sys
#import argparse
#from vtk.util.numpy_support import vtk_to_numpy, numpy_to_vtk
#import tkinter
#import tkinter.filedialog 
import os
#import matplotlib.pyplot as plt
import SimpleITK as sitk


def main():
	
	
	rootDir = "D:/Data_Scans/"
	outDir1 = "D:/Data_Scans/Scans_T/"
	inpDir= rootDir+"Scans_T"
	
	print("Processing >>>")
	for image in os.listdir(inpDir):
		filename = inpDir+"/"+image
		print(image)
		#read
		inputImage = sitk.ReadImage(filename)
		index=image.rindex(".nii")
		name=image[:index]
			
		#apply histogram equalization
		new_image1 = sitk.AdaptiveHistogramEqualization(inputImage, radius=[100,100,100], alpha=0, beta=1)
		
		#apply sharpness in the edge
		laplacian = sitk.LaplacianSharpeningImageFilter()
		img=laplacian.Execute(new_image1)
		
						
		#write new images
		dst_path1=outDir1+name+".nii"
		
		sitk.WriteImage(img, dst_path1)
		
		
		
		
	
		
	
	
	
if __name__ == '__main__':
    main()