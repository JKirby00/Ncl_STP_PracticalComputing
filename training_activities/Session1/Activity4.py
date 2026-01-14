'''File to be used for Activity 4 in session 1. In this
file you will find a function that has poorly chosen
variable names. Your task is to change these to be more
meaningful'''
from datetime import datetime
from matplotlib import pyplot as plt

def CodeWithPoorNames():
    '''This function uses variable names that are not
    very explanatory of what they are. Your task is
    to change them to more meaningful names. This
    function is not called in the mini PACS system
    so you will need to test it within this file 
    directly.'''
    # read in patient weight data
    with open(r"./training_activities_examples/Session1/Activity4_TestData.txt", "r") as f:
        l = f.readlines()

    # get the dates and weights
    d = l[0].split(",")
    w = l[1].split(",")

    # convert the types to date and float
    d_1, w_1 = [], []
    for q in d:
        d_1.append(datetime.strptime(q.strip("\n"), "%d/%m/%Y"))
        
    for a in w:
        w_1.append(float(a))

    # plot the data
    plt.plot(d_1, w_1)
    plt.ylabel("Weight (Kg)")
    plt.xlabel("Date")
    plt.show()



if __name__ == "__main__":
    CodeWithPoorNames()