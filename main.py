#sample med2image command:
#med2image -i 4week/Pig_530.nii -d out_test --reslice -t png
#med2image -i input_nii/Pig_530.nii -d 1out_test --outputFileType png  -s -1 --reslice

import os
import gzip

INPUT_FOLDER = "input_nii/"
MASK_IDENTIFIER = "-mask"

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
    gz_to_nii(INPUT_FOLDER + i, INPUT_FOLDER + i[:-3] + ".nii")
    os.remove(INPUT_FOLDER + i)
    
#========= med2image conversion =========#
