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

"""

import os
import sys
from glob import glob
import numpy as np
import signal
import gzip
import dill as pkl
from types import GeneratorType
time_given = int(15)

check_for_timeout = hasattr(signal, 'SIGALRM')


if check_for_timeout:
    def handler(signum, frame):
        raise TimeoutError(f"Timeout after {time_given}sec")
    signal.signal(signal.SIGALRM, handler)


ex_file = 'ex3.py'
full_points = 17
points = full_points
python = sys.executable

inputs = sorted(glob(os.path.join("unittest_input_*"), recursive=True))
inputs[0] = os.path.basename(inputs[0])

if not len(inputs):
    raise FileNotFoundError("Could not find unittest_input_* files")

feedback = ''

for test_i, input_folder in enumerate(inputs):
    input_folder = os.path.abspath(input_folder)
    comment = ''
    fcall = ''
    with open(os.devnull, 'w') as null:
        # sys.stdout = null
        try:
            if check_for_timeout:
                signal.alarm(time_given)
                from ex3 import ImageNormalizer
                signal.alarm(0)
            else:
                from ex3 import ImageNormalizer
            proper_import = True
        except Exception as e:
            outs = ''
            errs = e
            points -= full_points / len(inputs)
            proper_import = False
        finally:
            sys.stdout.flush()
            sys.stdout = sys.__stdout__
    
    if proper_import:
        with open(os.devnull, 'w') as null:
            # sys.stdout = null
            try:
                if check_for_timeout:
                    signal.alarm(time_given)
                    # check constructor
                    instance = ImageNormalizer(input_dir=input_folder)
                    fcall = f"ImageNormalizer(input_dir='{input_folder}')"
                    signal.alarm(0)
                else:
                    # check constructor
                    instance = ImageNormalizer(input_dir=input_folder)
                    fcall = f"ImageNormalizer(input_dir='{input_folder}')"
                errs = ''
                
                # check correct file names + sorting
                input_basename = os.path.basename(input_folder)
                with open(os.path.join(f"solutions", input_basename, f"filenames.txt"), 'r') as f:
                    filenames_so = f.read().replace('/', os.path.sep).splitlines()
                    if not (hasattr(instance, 'file_paths') and hasattr(instance, 'n_file_paths')):
                        points -= full_points / len(inputs) / 3
                        comment += f"Attributes 'file_paths' or 'n_file_paths' missing).\n"
                    elif instance.file_paths != filenames_so:
                        points -= full_points / len(inputs) / 3
                        comment += f"Attribute 'file_paths' should be {filenames_so} but is {instance.file_paths} (see directory 'solutions').\n"
                    elif instance.n_file_paths != len(filenames_so):
                        n_file_paths = len(filenames_so)
                        points -= full_points / len(inputs) / 3
                        comment += f"Attribute 'n_file_paths' should be {n_file_paths} but is {instance.n_file_paths} (see directory 'solutions').\n"
                
                # check if class has method analyze_images
                method = 'analyze_images'
                if not hasattr(instance, method):
                    comment += f'Method {method} missing.\n'
                    points -= full_points / len(inputs) / 3
                else:
                    # check for correct data types
                    stats = instance.analyze_images()
                    if (type(stats) is not tuple) or (len(stats) != 2):
                        points -= full_points / len(inputs) / 3
                        comment += f"Incorrect return value of method {method} (should be tuple of length 2).\n"
                    else:
                        with open(os.path.join(f"solutions", input_basename, f"mean_and_std.csv"), 'r') as fh:
                            m, s = fh.read().strip().split(',')
                            m, s = np.float64(m), np.float64(s)
                        if not (isinstance(stats[0], np.float64) and isinstance(stats[1], np.float64)):
                            points -= full_points / len(inputs) / 3
                            comment += f"Incorrect return data type of method {method} (tuple does not contain np.float64 values).\n"
                        else:
                            if not np.isclose(stats[0], m, atol=0):
                                points -= full_points / len(inputs) / 6
                                comment += f"Mean should be {m:.12f} but is {stats[0]:.12f} (see directory 'solutions').\n"
                            if not np.isclose(stats[1], s, atol=0):
                                points -= full_points / len(inputs) / 6
                                comment += f"Std should be {s:.12f} but is {stats[1]:.12f} (see directory 'solutions').\n"
                
                # check if class has method
                method = 'get_images_data'
                if not hasattr(instance, method):
                    comment += f'Method {method} missing.\n'
                    points -= full_points / len(inputs) / 3
                # check for correct data types
                elif not isinstance(instance.get_images_data(), GeneratorType):
                    points -= full_points / len(inputs) / 3
                    comment += f"{method} is not a generator.\n"
                else:
                    # Read correct image solutions
                    with gzip.open(os.path.join("solutions", input_basename, "images.pkl"), 'rb') as fh:
                        ims_sol = pkl.load(file=fh)
                    
                    # Get image submissions
                    ims_sub = list(instance.get_images_data())
                    
                    if not len(ims_sub) == len(ims_sol):
                        points -= full_points / len(inputs) / 3
                        comment += f"{len(ims_sol)} image arrays should have been returned but got {len(ims_sub)}.\n"
                    elif any([im_sub.dtype.num != np.dtype(np.float32).num for im_sub in ims_sub]):
                        points -= full_points / len(inputs) / 3
                        comment += f"Returned image arrays should have datatype np.float32 but at least one array isn't.\n"
                    else:
                        equl = [np.all(np.isclose(im_sub, im_sol, atol=0)) for im_sub, im_sol in zip(ims_sub, ims_sol)]
                        if not all(equl):
                            points -= full_points / len(inputs) / 3
                            comment += f"Returned images {list(np.where(np.logical_not(equl))[0])} do not match solution (see images.pkl files for solution).\n"
            except Exception as e:
                outs = ''
                errs = e
                points -= full_points / len(inputs)
            finally:
                sys.stdout.flush()
                sys.stdout = sys.__stdout__
    
    feedback += "#" * 6
    feedback += f" Test {test_i} "
    feedback += "#" * 6
    feedback += f"\nFunction call was:\n---\n{fcall}\n---\n"
    feedback += f"Error messages:\n---\n{errs}\n---\n"
    feedback += f"Comments:\n---\n{comment}\n---\n"
    feedback += f"Current points:{points:.2f}\n\n\n"

points = points if points > 0 else 0
feedback += "#" * 6
feedback += '''\nThis script doesn't guarantee your points, see "Instructions for submitting homework" for common mistakes.'''
if not check_for_timeout:
   feedback += "\n!!Warning: Had to switch to Windows compatibility version and did not check for timeouts!!"
print(f"{feedback}\n\nEstimated points: {points * 1:.4f}")
