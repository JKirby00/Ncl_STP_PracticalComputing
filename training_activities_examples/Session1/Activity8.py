'''File for Activity 8 in Session 1. The entry point
function is given but you may need to write additional
functions for this task.

Note - this example is VERY slow! it would be better to use built in
functions in various modules/packages but I have tried to avoid this
for this example.
'''

import pickle

def EstimateExternalVolume(px_arrs, slice_thickness,
    row_px_spacing, col_px_spacing, instance_numbers):
    '''This is the starting point for the activity 8 task to estimate
    the volume of the patient external on the imageset.
    
    Args:
        px_arrs (dict) = A dictionary where the keys are the instance
            numbers and the values are 2d pixel arrays
        slice_thickness (str) = The slice thickness in mm
        row_px_spacing (str) = The spacing between the central point
            of each pixel in mm (row spacing)
        col_px_spacing (str) = The spacing between the central point
            of each pixel in mm (column spacing)
        instance_numbers (list) = The list of image numbers. This effectively
            tells you the order of the images.

    returns: The calculated volume in cubic cms
    '''
    # order px arrays into a single list
    img_arr = []
    for num in instance_numbers:
        img_arr.append(px_arrs[str(num)].copy())
    
    masks = CreatePatientMask(img_arr = img_arr)

    vol = CalculateVolumeFromMasks(
        masks = masks,
        row_size = row_px_spacing,
        col_size = col_px_spacing,
        slice_spacing = slice_thickness)

    return round(vol, 1)

def CreatePatientMask(img_arr):
    '''Create a for each slice that represents the patient.
    If the pixel is inside the external set the pixel value to 1, 
    otherwise set value to 0.
    
    Args:
        img_arr (list) = List of arrays repesenting the image slices

    Returns:
        List of arrays where the pixel values have been transofmed to
        ones and zeros.
    '''
    masks = []# to add completed masks to

    count = 1
    for slice in img_arr:
        # loop through each slice
        print(f"Working on slice {count}")
        count += 1

        # get index of middle column of image
        mid_col = int(len(slice[0])/2.0)

        # working from the top in the middle, find the pixel
        # which first jumps in value by a given threshold
        max_val = slice.max()
        diff_thresh = 0.05*max_val

        for i in range(len(slice)):
            if abs(slice[i+1][mid_col] - slice[i][mid_col]) > diff_thresh:
                top_ind = i+1
                top_val = slice[i+1][mid_col]
                break

        # do a simple threshold
        slice[slice <= top_val] = 0
        slice[slice > top_val] = 1

        # now loop through and colour in zeros that are
        # inside the external
        for row in range(len(slice)):
            for col in range(len(slice[0])):
                if slice[row][col] == 0:
                    inside = CheckIfInside(
                        px_arr = slice,
                        row = row,
                        col = col
                    )

                    if inside is True:
                        slice[row][col] = 1

        masks.append(slice)
    
    return masks

def CheckIfInside(px_arr, row, col):
    '''Function to identify if the given pixel is inside the
    external or outside. It does this by assuming that there should
    be at least one pixel on each of up/down/left/right lines between this
    pixel and the edge of the dataset which is equal to 1 if the pixel
    is inside. The value of the pixel at row, col should be zero for this
    function to work.
    
    Args:
        px_arr (array) = pixel array for one slice
        row (int) = the row index
        col (int) = the col index

    returns True of False for inside or outside 
    '''
    up_empty, down_empty, left_empty, right_empty = True, True, True, True

    for i in range(0, row):
        if px_arr[i][col] == 1:
            up_empty = False

    if up_empty is True:
        # just return if this is True
        return False

    for i in range(row +1, len(px_arr)):
        if px_arr[i][col] == 1:
            down_empty = False

    if down_empty is True:
        # just return if this is True
        return False

    for i in range(0, col):
        if px_arr[row][i] == 1:
            left_empty = False

    if left_empty is True:
        # just return if this is True
        return False

    for i in range(col + 1, len(px_arr[0])):
        if px_arr[row][i] == 1:
            right_empty = False

    if right_empty is True:
        # just return if this is True
        return False
    
    # not yet returned so just return True
    return True

def CalculateVolumeFromMasks(masks, row_size, col_size, slice_spacing):
    '''Estimate the volume of the external based on the masked images
    along with the pixel size and slice thickness.'''
    # assume each pixel has volume of row_size * col_size * slice_thickness

    total_vol = 0
    for slice in masks:
        # find the number of pixels with value 1
        pxs = slice.sum()

        # calc vol (converting to cm from mm for each)
        slice_vol = pxs * (row_size/10.0) * (col_size/10.0) * (slice_spacing/10.0)
        total_vol = total_vol + slice_vol

    return total_vol
    
