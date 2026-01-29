'''File for Activity 7 of Session 1. This file contains a function
for calculating BMI. The name of the function is already set, you just
need to add the logic for calculating BMI within it.'''

def CalculateBMI(height, weight):
    '''Function to calculate BMI.
    
    Args:
        height (str) = The input height in metres
        width (str) = The input weight in kg

    Returns: The calculated BMI as a float
    '''
    # Note: Additional validation logic could be added to this
    # to check for whether height or weight are sensible values

    # first check that the height and weight can be converted to a float 
    try:
        height = float(height)
        weight = float(weight)
    except:
        return "Height or weight given is not a number"
    
    # calculate BMI
    bmi = weight / (height**2)

    return bmi