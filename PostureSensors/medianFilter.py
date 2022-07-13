import numpy as np

def median(readings):

    #arr = np.array(readings)
    sortedreadings = np.sort(readings)

    middleIndex = int((len(sortedreadings) - 1)/2)
    return sortedreadings[middleIndex]


    

  

#median([26.209712028503418, 28.981971740722656, 23.89540672302246, 46.08166217803955, 49.65534210205078])