# MultiNifti_to_png
Takes in multiple Nifti (.nii) files with masks and converts them into training and validation datasets for use in Machine Learning / Deep Learning image segmentation.

Currently this will be tailored for image segmentation work with masks but the overall goal is to have this tool be able to pre-process images for any type of nii files for use in AI applications. 

## TODO
- [ ] Convert multiple nii files into corresponding slices stored sequentially
- [ ] Automatic splitting of the generated images into training and validation datasets with corresponding masks 
- [ ] Extract files stored in compressed formats