import numpy as np
import math

def khi2(crosstab):
    d = crosstab.shape
    if (len (d)  > 2):
        raise("Wrong format for this function")
    rows=d[0]  # unnecessary, but clear
    cols=d[1]  # unnecessary, but clear
    print("Degrees of freedom: ",(rows-1)*(cols-1))
    print("Marginal sums:")
    expecteds=margins3(crosstab)
    print(expecteds)
    for k in range(rows):
        for l in range(cols):
            expecteds[k,l]=expecteds[k,cols]*expecteds[rows,l]/expecteds[rows,cols]
    print("Expected values:")
    print(expecteds)
    sum = 0
    deviation=np.zeros((rows+1,cols+1))
    for k in range(rows):
        for l in range(cols):
            deviation[k,l]=((expecteds[k,l]-crosstab[k,l]))
            sum += deviation[k,l]**2/expecteds[k,l]
    print(crosstab)
    print(deviation)
    print(sum)



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
