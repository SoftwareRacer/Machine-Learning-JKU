"""
Author -- Michael Widrich
Contact -- widrich@ml.jku.at
Date -- 01.03.2020

###############################################################################

The following copyright statement applies to all code within this file.

Copyright statement:
This  material,  no  matter  whether  in  printed  or  electronic  form,
may  be  used  for personal  and non-commercial educational use only.
Any reproduction of this manuscript, no matter whether as a whole or in parts,
no matter whether in printed or in electronic form, requires explicit prior
acceptance of the authors.

###############################################################################

This script will take a folder input_path and rescale all .jpg images in it to
a resolution such that the file size is ~850kB or smaller.
Note that the new file size is typically much smaller due to .jpg compression
but that will not bother us as long as the content is not too blurry.
The resulting image files will be written to folder input_path + "_small".

Requirements: You will need the pillow package (pip3 install pillow).

Usage: Set input_path to the path containing your .jpg files.
"""

import os
import shutil
import glob
from tqdm import tqdm
from PIL import Image  # Use pillow for image processing

input_path = "C:\Users\marco\Documents\Schule\_Mech_2S\Python\supplements_ex1\example_jpgs"
# Output folder should have the same names as the input folder but with "_small" added at the end of the folder name.
# Note that the following line will work even if input_path has a trailing "/" character.
output_path = input_path + "_small"
# We want files with max. 850 kB = 850 kilo Byte (= 850 * 1000 * 8 bit)
desired_file_size = 850e3
# Get list of files
image_files = glob.glob(os.path.join(input_path, '*.jpg'))
# Make output directory
os.makedirs(output_path)

for image_file in tqdm(image_files, desc="Processing files"):
    # Get size of file in Bytes
    file_size = os.path.getsize(image_file)
    # Calculate reduction factor
    reduction_factor = desired_file_size / file_size
    # We want to apply rescaling factor to x and y dimension -> 2D -> we need to apply the square-root
    reduction_factor = reduction_factor ** (1./2)
    
    # Only change image resolution if we need to reduce the file size
    if reduction_factor < 1:
        # Read file
        image = Image.open(image_file)
        # Get current resolution
        old_size = image.size
        # Calculate new file-size
        new_size = [int(s * reduction_factor) for s in old_size]
        # Resize to new_size and save image in new folder
        new_image = image.resize(new_size)
        new_image.save(os.path.join(output_path, os.path.basename(image_file)))
    else:
        # If the file size is already small enough, we can just copy the file
        shutil.copy(image_file, os.path.join(output_path, os.path.basename(image_file)))
