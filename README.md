# MultiNifti_to_png
Takes in multiple Nifti (.nii) files with masks and converts them into training and validation datasets for use in Machine Learning / Deep Learning image segmentation.

Currently this will be tailored for image segmentation work with masks but the overall goal is to have this tool be able to pre-process images for any type of nii files for use in AI applications. 

## Installation

For installing this script you need to use the latest version of python and pip. It is recommended to run this in a virtual environment (venv)

To install the dependencies run:
```pip3 install -r requirements.txt```

Please make sure to have the initial file locations and such changed accordingly in the main.py file before running the script. All file location variables will be in CAPITAL_SNAKECASE format.

To run the script:
```python3 main.py```

## TODO
- [ ] Convert x, y, z data into training and validation sets
- [ ] Granular options to select what axis to convert
- [ ] CLI interface
- [ ] Account for outlier input data + edge cases
- [ ] Duplicate file checking
- [x] Convert multiple nii files into corresponding slices stored sequentially
- [x] Automatic splitting of the generated images into training and validation datasets with corresponding masks 
- [x] Extract files stored in compressed formats (.gz)

## Resources
 - Med2Image (https://github.com/FNNDSC/med2image)