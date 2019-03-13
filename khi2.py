import numpy as np
from logger import logger
import math

def khi2(crosstab, loglevel=False):
    d = crosstab.shape
    if (len (d)  > 2):
        raise("Wrong format for this function")
    rows=d[0]  # unnecessary, but clear
    cols=d[1]  # unnecessary, but clear
    streng = "Degrees of freedom: " + str((rows-1)*(cols-1))
    streng += "Marginal sums:\n"
    expecteds = margins3(crosstab)
    streng += str(expecteds)
    for k in range(rows):
        for l in range(cols):
            expecteds[k,l]=expecteds[k,cols]*expecteds[rows,l]/expecteds[rows,cols]
    streng += "\nExpected values:\n"
    streng += str(expecteds) + "\n"
    sum = 0
    deviation = np.zeros((rows+1,cols+1))
    for k in range(rows):
        for l in range(cols):
            deviation[k,l]=((expecteds[k,l]-crosstab[k,l]))
            sum += deviation[k,l]**2/expecteds[k,l]
    streng += str(crosstab) + "\n" + str(deviation) + "\n" + str(sum) + "\n"
    logger(streng, loglevel)
    return sum


def margins3 (a):
    d = a.shape
    if (len (d)  > 2):
        raise("Wrong format for this function")
    rows=d[0]  # unnecessary, but clear
    cols=d[1]  # unnecessary, but clear
    margins = np.zeros((rows+1,cols+1))
    for i in range(rows):
        margins[i,cols] = a[i].sum()
    for j in range(cols):
        margins[rows,j] = a[:,j].sum()
    margins[rows,cols] = margins[:,cols].sum()
    return margins
