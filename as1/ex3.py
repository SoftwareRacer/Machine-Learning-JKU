# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 21:01:28 2021

@author: Admin
"""

import os
import PIL.Image
import numpy as np

dirname = os.path.dirname(__file__) #Absolute path of the file 
rel_inp_dirname = os.path.join(dirname, 'files') #relative path of resources

class ImageNormalizer:
    file_paths = []
    n_file_paths = 0
    mean = None
    std = None
    
    def __init__(input_dir):
        fileNames = os.listdir(input_dir) #get file names
        sorted(fileNames)
        for fileName in fileNames:
            old_path = os.path.join(input_dir, fileName) #safes old path
            if os.path.isdir(old_path):
                ImageNormalizer.__init__(old_path) #if path links to directory, reexecute the function for this folder
            if os.path.isfile(old_path.endswith(".jpeg") or old_path.endswith(".jpg") or old_path.endswith(".JPG") or old_path.endswith(".JPEG")): #1. condition
                ImageNormalizer.file_paths.append(fileName)
                ImageNormalizer.n_file_paths += 1
 
    def analyze_images():
        for fileName in ImageNormalizer.file_paths:
            ImageNormalizer.mean.append(np.mean(fileName)) #adds mean value of file to array of means
            ImageNormalizer.std.append(np.std(fileName)) #adds std deviation of file to array of std deviations
        ImageNormalizer.mean = ImageNormalizer.mean.astype(np.float64) #defines type to np.float64
        ImageNormalizer.std = ImageNormalizer.std.astype(np.float64)
        
        return (ImageNormalizer.mean, ImageNormalizer.std) #returns tuple of mean and standard deviation
        
    def get_images_data():
        counter = 0
        try:
            for fileName in ImageNormalizer.file_paths:
                image = PIL.Image.open(fileName)
                pixels = np.asarray(image)
                pixels = pixels.astype(np.float32) #defines each pixel as np.float32
                pixels -= ImageNormalizer.mean
                pixels /= ImageNormalizer.std 
                yield pixels # returns operated pixels
                counter += 1
        except ValueError:
            print("Error! mean or std is None")
            
