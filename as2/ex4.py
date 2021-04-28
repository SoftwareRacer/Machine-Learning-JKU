# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 18:54:46 2021

Author: Marco Hennermann
Matr.nr.: K11911555
Exercise: 4
"""
import os
import PIL.Image
import numpy as np
import shutil as shutil
import logging
from statistics import variance

dirname = os.path.dirname(__file__) #Absolute path of the file 
rel_inp_dirname = os.path.join(dirname, 'files') #relative path of resources
rel_out_dirname = os.path.join(dirname, 'new_files') #path where processed files get stored
list_of_incorrect_files = [] 
'''
 fileNames = os.listdir(inp_dir) #get file names
        sorted(fileNames)
        ser_num = 1
        output_file_list = []
        err = 0
        if not out_dir:
            os.mkdir(out_dir) #if output-directory doesn't exist, make it
        if not logfile:
            logfile = open("logfile.txt","w+") #if logfile doesn't exist, make it
        for fileName in fileNames:
            old_path = os.path.join(inp_dir, fileName) #safes old path
            if os.path.isdir(old_path):
                ex2(old_path, out_dir, logfile) #if path links to directory, reexecute the function for this folder
            if not os.path.isfile(out_dir + "/" + str(ser_num).zfill(7)) and (old_path.endswith(".jpeg") or old_path.endswith(".jpg") or old_path.endswith(".JPG") or old_path.endswith(".JPEG")): #1. condition
         '''   
def ex4(image_array, border_x, border_y):
    try:
        input_array = image_array
        target_array = []
        for i in range(0, border_x[0]):
            for j in range(0, len(input_array[1,:])):
                input_array[i][j] = 0
                target_array += image_array[i][j]
        for i in range(len(input_array[:,1])-border_x[1], len(input_array[:,1])):
            for j in range(0, len(input_array[1,:])):
                input_array[i][j] = 0
                target_array += image_array[i][j]
        for i in range(0, border_y[0]):
            for j in range(0, len(input_array[:,1])):
                input_array[j][i] = 0
                target_array += image_array[i][j]
        for i in range(len(input_array[1,:])-border_y[1], len(input_array[1,:])):
            for j in range(0, len(input_array[:,1])):
                input_array[j][i] = 0
                target_array += image_array[i][j]
       
        known_array = input_array
        for i in range(len(known_array[:,1])):
            for i in range(len(known_array[1,:])):
                if(known_array[i][j] != 0):
                    known_array[i][j] = 1
    except NotImplementedError as nie:
        print("image_array is not a 2D-numpy-array")
        logging.error(nie)
    except ValueError as ve:
        print("border_x or border_y are no correct int-values")            
        logging.error(ve)
    