'''Example code for Activity 3 in session 1. 
This is the code after being re-factored into units.'''
import numpy as np

def FindInstanceNumbersForPercent(inst_num_list, percent_list):
    '''Function to find the closest instance numbers
    for a given percentage of the way between the min
    and max instance number.
    
    Args:
        inst_num_list (list) = list of instance numbers
        percent_list (list) = list of percentages to find
            number for

    returns list of instance numbers
    '''
    inst_range = max(inst_num_list) - min(inst_num_list)
    min_instance = min(inst_num_list)

    return_inst_nums = []
    for perc in percent_list:
        val = int((perc/100.0)*inst_range + min_instance)
        return_inst_nums.append(val)

    return return_inst_nums

def CalculateBasicData(px_arr, image_number):
    '''Function to calculate the min, max and mean
    pixel values on an array and to print this to the console
    
    Args:
        px_arr (array) = The array of pixel values
        image_number (int) = The image number

    returns nothing
    '''
    print(f"For image number: {image_number}")
    print(f"Minimum pixel value: {px_arr.min()}")
    print(f"Maximum pixel value: {px_arr.max()}")
    print(f"Mean pixel value: {round(px_arr.mean(), 1)}")
    print("\n")

def CalculatePixelWeightingFactor(px_arr):
    '''Function to calculate the pixel weighing factor
    and return this
    
    Args:
        px_arr (array) = Array of pxel data

    Returns (int) = The calculated pixel weighting factor
    '''
    # convert to 64bit to have large enough numbers
    px_arr = np.array(px_arr, dtype = np.int64)

    # return weighting factor
    return np.sum(px_arr**2)

def GetSomeImageStats(image_data):
    '''
    This is function that find some slightly random image
    information from the image data and then prints
    it to the console.

    Args:
        image_data (dict) = Dict of image data with keys "instance_ids"
            [which is a list of integers] and "images" [which is another
            dict where the key is the instance id and the value is an
            array representing the pixel data]

    returns nothing 
    '''
    print("################")
    print("Session 1 Activity 3 Image Data Stats:")

    # find the instance numbers that are 25%, 50% and 75% of the way through
    # the image set
    percent_list = [25, 50, 75]
    inst_nums = FindInstanceNumbersForPercent(
        inst_num_list = image_data["instance_ids"],
        percent_list = percent_list)

    # calculate basic image stats and print them
    for inst_num in inst_nums:
        CalculateBasicData(
            px_arr = image_data["images"][str(inst_num)],
            image_number = inst_num)

    # calculate pixel weighting factors and print them
    print("Pixel weighting factors:")
    for i in range(len(percent_list)):
        factor = CalculatePixelWeightingFactor(
            px_arr= image_data["images"][str(inst_nums[i])])
        
        print(f"{percent_list[i]}% image: {factor}")

    print("#########################")

if __name__ == "__main__":
    # so that you can test it without having to run the whole pacs system
    # each time, load some test data from a pickle file in the repository
    import pickle

    with open(r"./training_activities_examples/Session1/Activity3_TestData.pkl", "rb") as f:
        image_data = pickle.load(f)

    GetSomeImageStats(image_data = image_data)