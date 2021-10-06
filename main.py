#sample med2image command:
#med2image -i 4week/Pig_530.nii -d out_test --reslice -t png

import os
import gzip

INPUT_FOLDER = "4week/"

files_input_folder = os.listdir()
compressed_files = [f for f in os.listdir(INPUT_FOLDER) if ".gz" in f]

def gunzip(source_filepath, dest_filepath, block_size=65536):
    with gzip.open(source_filepath, 'rb') as s_file, \
            open(dest_filepath, 'wb') as d_file:
        while True:
            block = s_file.read(block_size)
            if not block:
                break
            else:
                d_file.write(block)

gunzip(INPUT_FOLDER + compressed_files[0], "test.nii")


print(compressed_files)