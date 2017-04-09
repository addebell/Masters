__author__ = 'ollie'
from Structure import *

#test

Alldata  = pkl.load(open("processeddata.p"))

inv10 = [run for run in Alldata if run.day == '10']
inv11b = [run for run in Alldata if run.day == '11b']
inv12 = [run for run in Alldata if run.day == '12']
investigations = [inv10,inv11b,inv12]




def plotcoolrates ():
    for investigation in investigations:
       for run in investigation:
            col = run.colour() + 'o'
            plt.plot(run.coolingrate(),run.freezetemp,col)
    plt.show()

plotcoolrates()