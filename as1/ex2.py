# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 16:44:06 2021

@author: Marco Hennermann, K11911555
"""

import os
import PIL.Image
import numpy as np
import shutil as shutil
from statistics import variance

dirname = os.path.dirname(__file__) #Absolute path of the file 
rel_inp_dirname = os.path.join(dirname, 'files') #relative path of resources
rel_out_dirname = os.path.join(dirname, 'new_files') #path where processed files get stored
list_of_incorrect_files = [] 

def ex2(inp_dir, out_dir, logfile):
    try:
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
                if os.path.getsize(old_path) > 10e3: #2. condition
                    try: #3. condition
                        im = PIL.Image.open(old_path)
                        width, height, color = np.shape(np.array(im))
                        
                        if width >= 100 and height >= 100 and color > 0: #4. condition
                            if variance(im) > 0: #5. condition
                                if not find_duplicate_images(im, output_file_list): #6. condition
                                    output_file_list.append(out_dir + "/" + str(ser_num).zfill(7) + ".jpg")
                                    print(out_dir + "/" + str(ser_num).zfill(7) + ".jpg")
                                    shutil.copy(old_path, out_dir + "/" + str(ser_num).zfill(7) + ".jpg")
                                    ser_num += 1                     
                                else:
                                    err = 6
                                    list_of_incorrect_files.append(old_path + ";" + str(err) + "\n")
                                    continue
                            else:
                                err = 5
                                list_of_incorrect_files.append(old_path + ";" + str(err) + "\n")
                                continue
                        else:
                            err = 4
                            list_of_incorrect_files.append(old_path + ";" + str(err) + "\n")
                            continue
                    except IOError:
                        err = 3
                        list_of_incorrect_files.append(old_path + ";" + str(err) + "\n")
                        continue                  
                else: 
                    err = 2
                    list_of_incorrect_files.append(old_path + ";" + str(err) + "\n")
                    continue
            else:
                err = 1
                list_of_incorrect_files.append(old_path + ";" + str(err) + "\n")
                continue
        for i in range(len(list_of_incorrect_files)):
            logfile.write(list_of_incorrect_files[i]) #writes errors to logfile
    except Exception as e:
        print(e)
    return ser_num-1

def find_duplicate_images(fileName, output_file_list):
    for file in output_file_list:
        if compare_images(fileName, file):
            return True
    return False

def compare_images(input_image, output_image):
  rows, cols, color = np.shape(np.array(output_image))

  # compare image pixels
  for row in range(rows):
    for col in range(cols):
      input_pixel = input_image.getpixel((row, col))
      output_pixel = output_image.getpixel((row, col))
      if input_pixel != output_pixel:
        return False
  return True

if __name__ == '__main__':
    num_of_files = ex2(rel_inp_dirname, rel_out_dirname, list_of_incorrect_files)
    print(str(num_of_files) + " files moved successfully")