'''File for Activity 5 of Session 1. In this activity,
the function given does not have a docstring or any
comments. Your task is to add them in.'''


def CalculateStrightLineBetweenPoints(data):
    coords = data.split("),(")

    coords[0] = coords[0].strip("(")
    coords[-1] = coords[-1].strip(")")

    grad_ints = []

    for i in range(len(coords)):
        coords[i] = coords[i].split(",")
        coords[i][0] = float(coords[i][0])
        coords[i][1] = float(coords[i][1])

    for i in range(len(coords)):
        if i == len(coords) - 1:
            continue

        y_diff = coords[i+1][1] - coords[i][1]
        x_diff = coords[i+1][0] - coords[i][0]

        grad = y_diff/x_diff
        int = coords[i][1] - (grad*coords[i][0])

        grad_ints.append([grad, int])

    return grad_ints

if __name__ == "__main__":
    result = CalculateStrightLineBetweenPoints(
        data = "(0,1),(0.5,2),(1,3),(1.5,4),(2,5)"
    )

    print(result)