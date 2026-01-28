'''This is the file for Activity 3 in Session 1. This currently
contains a single long function. You task is to split it up into
smaller units that work together to give the same functionality.'''

import numpy as np

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
    max_instance = max(image_data["instance_ids"])
    min_instance = min(image_data["instance_ids"])

    inst_25 = int(0.25*(max_instance - min_instance) + min_instance)
    inst_50 = int(0.5*(max_instance - min_instance) + min_instance)
    inst_75 = int(0.75*(max_instance - min_instance) + min_instance)

    # for each of these slices find some stats and print them to the screen
    # find the min pixel values
    px_min_inst_25 = image_data["images"][str(inst_25)].min()
    px_min_inst_50 = image_data["images"][str(inst_50)].min()
    px_min_inst_75 = image_data["images"][str(inst_75)].min()

    # find the max pixel values
    px_max_inst_25 = image_data["images"][str(inst_25)].max()
    px_max_inst_50 = image_data["images"][str(inst_50)].max()
    px_max_inst_75 = image_data["images"][str(inst_75)].max()
    
    # find the mean pixel values
    px_mean_inst_25 = image_data["images"][str(inst_25)].mean()
    px_mean_inst_50 = image_data["images"][str(inst_50)].mean()
    px_mean_inst_75 = image_data["images"][str(inst_75)].mean()

    print(f"For image number: {inst_25}")
    print(f"Minimum pixel value: {px_min_inst_25}")
    print(f"Maximum pixel value: {px_max_inst_25}")
    print(f"Mean pixel value: {round(px_mean_inst_25, 1)}")
    print("\n")
    print(f"For image number: {inst_50}")
    print(f"Minimum pixel value: {px_min_inst_50}")
    print(f"Maximum pixel value: {px_max_inst_50}")
    print(f"Mean pixel value: {round(px_mean_inst_50,1)}")
    print("\n")
    print(f"For image number: {inst_75}")
    print(f"Minimum pixel value: {px_min_inst_75}")
    print(f"Maximum pixel value: {px_max_inst_75}")
    print(f"Mean pixel value: {round(px_mean_inst_75, 1)}")
    print("\n")

    # find the fictional pixel weighting factor for each of the
    # three slices (factor = the sum of the squared pixel values)
    px_weighting_factor_25 = np.sum(np.array(image_data["images"][str(inst_25)], dtype = np.int64)**2)
    px_weighting_factor_50 = np.sum(np.array(image_data["images"][str(inst_50)], dtype = np.int64)**2)
    px_weighting_factor_75 = np.sum(np.array(image_data["images"][str(inst_75)], dtype = np.int64)**2)

    print("Pixel weighting factors:")
    print(f"25% image: {px_weighting_factor_25}")
    print(f"50% image: {px_weighting_factor_50}")
    print(f"75% image: {px_weighting_factor_75}")

    print("#########################")

if __name__ == "__main__":
    # so that you can test it without having to run the whole pacs system
    # each time, load some test data from a pickle file in the repository
    import pickle

    with open(r"./training_activities_examples/Session1/Activity3_TestData.pkl", "rb") as f:
        image_data = pickle.load(f)

    GetSomeImageStats(image_data = image_data)