import numpy as np

def median(readings):

    sortedreadings = np.sort(readings)

    middleIndex = int((len(sortedreadings) - 1)/2)
    return sortedreadings[middleIndex]
