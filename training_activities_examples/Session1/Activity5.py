'''File for Activity 5 of Session 1. In this activity,
the function given does not have a docstring or any
comments. Your task is to add them in.'''


def CalculateStrightLineBetweenPoints(data):
    '''Function that calculates the gradient and intercept
    of a straight line between each adjacent set of
    points within a string containing a list of coordinates.
    
    Args:
        data (str) = A string containing a list of comma
            separate coorindates e.g. "(x,y),(x,y),(x,y)"

    Returns:
        A list of lists where each child list contains the gradient
        and intercept between the i and i+1 coordinates.
    '''
    # split the string and strip start and end brackets
    coords = data.split("),(")
    coords[0] = coords[0].strip("(")
    coords[-1] = coords[-1].strip(")")

    # create a blank list to add the gradient and intercepts
    grad_ints = []

    # split the coordinate string again and convert to float
    for i in range(len(coords)):
        coords[i] = coords[i].split(",")
        coords[i][0] = float(coords[i][0])
        coords[i][1] = float(coords[i][1])

    for i in range(len(coords)):
        if i == len(coords) - 1:
            # ignore the last coord as there is
            # nothing after it
            continue

        # calculate the gradient and intercept
        y_diff = coords[i+1][1] - coords[i][1]
        x_diff = coords[i+1][0] - coords[i][0]

        grad = y_diff/x_diff
        int = coords[i][1] - (grad*coords[i][0])

        # add the gradient and intercept to the list
        grad_ints.append([grad, int])

    return grad_ints

if __name__ == "__main__":
    result = CalculateStrightLineBetweenPoints(
        data = "(0,1),(0.5,2),(1,3),(1.5,4),(2,5)"
    )

    print(result)