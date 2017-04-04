__author__ = 'ollie'

import numpy as np
import pickle as pkl
import csv
import matplotlib.pyplot as plt
import scipy.stats as stats
import scipy.optimize as opt


#data = np.array([[0.0, 1.25, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 8.5, 8.51],
 #[8.4, 2.1, -0.6, -2.8, -4.9, -6.3, -7, -7.4, -7.6, -7.7, 0],
 #[12.27, -8.64, -9.92, -10.54, -10.65, -10.62, -10.57, -10.54, -10.53, -10.52, None]])

def restrictdata (data,threshold = 1.0):
    times,cuvette,plate =  list(data[0]),list(data[1]),list(data[2])

    difference = 10.0
    while difference >= threshold:
        i = 0
        times.pop(0)
        cuvette.pop(0)
        plate.pop(0)
        try:
            difference = plate[i] - plate[-1]
        except TypeError:
            try:
                difference = plate[i] - plate[-2]
            except TypeError:
                try:
                    difference = plate[i] - plate[-3]
                except: pass
        i+=1
    while cuvette[-1] >= -1.0:
        times.pop()
        cuvette.pop()
        plate.pop()
    return np.array([times,cuvette,plate])

def function (asyptoticT,*args):
    data = [list(args[0]),list(args[1])]
    temps = np.array(data[1])-asyptoticT
    x = np.array(data[0])
    y = np.log(temps)
    out = np.polyfit(x,y,1,full=True)
    return out[1]


def determineasymptT (data):
    lower = min([x for x in data[2] if x is not None])+0.01
    upper = min ([x for x in data[1] if x is not None])-0.01

    minTs = [None]
    for T in np.arange(lower,upper,0.007):
        previous = function(T+0.007,*data)
        point = function(T,*data)
        next = function(T-0.007,*data)

        if point < previous and point < next:
            minTs.append(T)

    return minTs[-1]



'''
for n in np.arange(-7.5,-20.,-0.05):
    plt.plot(n,function(n,data),'bo')
plt.show()
'''


def coolrate (data,asyptoticT):
    data = [list(data[0]),list(data[1])]
    temps = np.array(data[1])-asyptoticT
    x = np.array(data[0])
    y = np.log(temps)
    out = np.polyfit(x,y,1)
    return -out[0]
