#sample med2image command:
#med2image -i 4week/Pig_530.nii -d out_test --reslice -t png
#med2image -i input_nii/Pig_530.nii -d 1out_test --outputFileType png  -s -1 --reslice

import os
import gzip
import shutil
import threading

INPUT_FOLDER = "4week/"
MASK_IDENTIFIER = "-mask"
THREADED = True
MULTI_AXIS = False
TRAIN_VAL_SPLIT = .8

#========= gz compressed file conversion =========#

compressed_files = [f for f in os.listdir(INPUT_FOLDER) if ".gz" in f]

def gz_to_nii(source_filepath, dest_filepath, block_size=65536):
    with gzip.open(source_filepath, 'rb') as s_file, \
            open(dest_filepath, 'wb') as d_file:
        while True:
            block = s_file.read(block_size)
            if not block:
                break
            else:
                d_file.write(block)
    print("Converted - " + source_filepath + " to " + dest_filepath)


for i in compressed_files:
    gz_to_nii(INPUT_FOLDER + i, INPUT_FOLDER + i[:-3])
    os.remove(INPUT_FOLDER + i)
    
#========= med2image conversion =========#

nii_files = os.listdir(INPUT_FOLDER)

#Of the files that have .nii in them filter out if it does or doesn't have the MASK_IDENTIFIER in them
pig_nii = [f for f in [f for f in nii_files if ".nii" in f] if MASK_IDENTIFIER not in f]
mask_nii = [f for f in [f for f in nii_files if ".nii" in f] if MASK_IDENTIFIER in f]

def med2image_run(input_dir, output_dir, filetype, file_stem, reslice):
    if reslice:
        os.system("med2image -i " + input_dir + " -d " + output_dir + " --outputFileType " + filetype + " -o " + file_stem + " -s -1 --reslice")
    else:
        os.system("med2image -i " + input_dir + " -d " + output_dir + " --outputFileType " + filetype + " -o " + file_stem + "  -s -1")
        
testing_file_num = 1

#Pig files 
RAW_FOLDER_PIG = "pig_nii_raw/"
if os.path.exists(RAW_FOLDER_PIG):
    shutil.rmtree(RAW_FOLDER_PIG)
os.mkdir(RAW_FOLDER_PIG)
pig_nii_threads = []
for i in pig_nii[:testing_file_num]:
    #med2image_run(INPUT_FOLDER+i, "pig_nii_raw", "png", True)
    pig_nii_threads.append(threading.Thread(target=med2image_run, args=(INPUT_FOLDER+i, "pig_nii_raw", "png", i[:-4], MULTI_AXIS)))

if THREADED:
    for i in pig_nii_threads:
        i.start()

    for i in pig_nii_threads:
        i.join()

#Mask files
RAW_FOLDER_MASK = "mask_nii_raw/"
if os.path.exists(RAW_FOLDER_MASK):
    shutil.rmtree(RAW_FOLDER_MASK)
mask_nii_threads = []
os.mkdir(RAW_FOLDER_MASK)
for i in mask_nii[:testing_file_num]:
    #med2image_run(INPUT_FOLDER+i, "mask_nii_raw", "png", True)
    mask_nii_threads.append(threading.Thread(target=med2image_run, args=(INPUT_FOLDER+i, "mask_nii_raw", "png", i[:-4], MULTI_AXIS)))

if THREADED:
    for i in mask_nii_threads:
        i.start()

    for i in mask_nii_threads:
        i.join()

#========= Convert into training/validation =========#

TRAIN_FOLDER = "pig_nii_train/"
VALIDATE_FOLDER = "pig_nii_val/"
if os.path.exists(TRAIN_FOLDER):
    shutil.rmtree(TRAIN_FOLDER)
os.mkdir(TRAIN_FOLDER)
if os.path.exists(VALIDATE_FOLDER):
    shutil.rmtree(VALIDATE_FOLDER)
os.mkdir(VALIDATE_FOLDER)

pig_files = os.listdir(RAW_FOLDER_PIG)
mask_files = os.listdir(RAW_FOLDER_MASK)

num_train = int(len(pig_files) * TRAIN_VAL_SPLIT)-1
num_val = len(pig_files) - num_train - 1


if os.path.exists(TRAIN_FOLDER + "image"):
    shutil.rmtree(TRAIN_FOLDER + "image")
os.mkdir(TRAIN_FOLDER + "image")
if os.path.exists(TRAIN_FOLDER + "segmentation"):
    shutil.rmtree(TRAIN_FOLDER + "segmentation")
os.mkdir(TRAIN_FOLDER + "segmentation")
for i in range(0, num_train):
    shutil.move(RAW_FOLDER_PIG + pig_files[i] , TRAIN_FOLDER + "image/" + pig_files[i])
    shutil.move(RAW_FOLDER_MASK + mask_files[i] , TRAIN_FOLDER + "segmentation/" + mask_files[i])


if os.path.exists(VALIDATE_FOLDER + "image"):
    shutil.rmtree(VALIDATE_FOLDER + "image")
os.mkdir(VALIDATE_FOLDER + "image")
if os.path.exists(VALIDATE_FOLDER + "segmentation"):
    shutil.rmtree(VALIDATE_FOLDER + "segmentation")
os.mkdir(VALIDATE_FOLDER + "segmentation")
for i in range(num_train, num_val):
    shutil.move(RAW_FOLDER_PIG + pig_files[i] , VALIDATE_FOLDER + "image/" + pig_files[i])
    shutil.move(RAW_FOLDER_MASK + mask_files[i] , VALIDATE_FOLDER + "segmentation/" + mask_files[i])