#sample med2image command:
#med2image -i 4week/Pig_530.nii -d out_test --reslice -t png
#med2image -i input_nii/Pig_530.nii -d 1out_test --outputFileType png  -s -1 --reslice

import os
import gzip
import shutil
import threading

INPUT_FOLDER = "input_nii/"
MASK_IDENTIFIER = "-mask"
THREADED = True

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

def med2image_run(input_dir, output_dir, filetype, reslice):
    if reslice:
        os.system("med2image -i " + input_dir + " -d " + output_dir + " --outputFileType " + filetype + "  -s -1 --reslice")
    else:
        os.system("med2image -i " + input_dir + " -d " + output_dir + " --outputFileType " + filetype + "  -s -1")
        
testing_file_num = 2

shutil.rmtree("pig_nii_raw")
os.mkdir("pig_nii_raw")
pig_nii_threads = []
for i in pig_nii[:testing_file_num]:
    #med2image_run(INPUT_FOLDER+i, "pig_nii_raw", "png", True)
    pig_nii_threads.append(threading.Thread(target=med2image_run, args=(INPUT_FOLDER+i, "pig_nii_raw", "png", True)))

if THREADED:
    for i in pig_nii_threads:
        i.start()

    for i in pig_nii_threads:
        i.join()

shutil.rmtree("mask_nii_raw")
mask_nii_threads = []
os.mkdir("mask_nii_raw")
for i in mask_nii[:testing_file_num]:
    #med2image_run(INPUT_FOLDER+i, "mask_nii_raw", "png", True)
    mask_nii_threads.append(threading.Thread(target=med2image_run, args=(INPUT_FOLDER+i, "mask_nii_raw", "png", True)))

if THREADED:
    for i in mask_nii_threads:
        i.start()

    for i in mask_nii_threads:
        i.join()