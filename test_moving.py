import os
import gzip
import shutil
import threading

INPUT_FOLDER = "4week/"
MASK_IDENTIFIER = "-mask"
THREADED = True
MULTI_AXIS = False
TRAIN_VAL_SPLIT = .8

RAW_FOLDER_PIG = "pig_nii_raw/"
RAW_FOLDER_MASK = "mask_nii_raw/"


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
num_val = len(pig_files) - 1


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

print(num_train)
print(num_val)