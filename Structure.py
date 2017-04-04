__author__ = 'ollie'

import numpy as np
import pickle as pkl
import csv
import matplotlib.pyplot as plt
import scipy.stats as stats
import ast
import rates as rates
import time

class Run :
    def __init__(self, data,frequency=0,settemp = 0, ambientgun=0,ambientthermometer = 0,timeofday = 0, day = 0,runnumber = 0):
        self.data = data
        self.frequency = frequency
        self.ambientgun = ambientgun
        self.ambientthermometer = ambientthermometer
        self.timeofday = timeofday
        self.day = day
        self.__coolingrate = 0
        self.__asymptotictemp = 0
        self.settemp = settemp
        self.runnumber = runnumber
        self.freezetemp = min(data[1][-3:])

    def coolingrate (self):
        if self.__coolingrate == 0:
            self.findrates()
        return self.__coolingrate

    def asymptotictemp (self):
        if self.__coolingrate == 0:
            self.findrates()
        return self.__asymptotictemp

    def findrates (self):
        restricteddata = rates.restrictdata(self.data)
        #try:
        self.__asymptotictemp = rates.determineasymptT(restricteddata)
        if self.__asymptotictemp is not None:
            self.__coolingrate = rates.coolrate(restricteddata,self.__asymptotictemp)
        else: self.__coolingrate = None

    def colour(self):
        if self.frequency == 'Cal':
            self.__colour = 'b'
        elif self.frequency == 'DC':
            self.__colour = 'y'
        else: self.__colour = 'r'
        return self.__colour

    def __repr__(self):
        return 'Run'+repr(self.runnumber)+' on investigation'+repr(self.day)

    def plotcooling(self):
        plt.plot(self.data[0],self.data[1],'r--')
        plt.plot(self.data[0],self.data[2],'b-')

    def plotlogcoolcurve(self):
        d = rates.restrictdata(self.data)
        temps = np.array(d[1])-self.asymptotictemp()
        x = np.array(d[0])
        y = np.log(temps)
        col = self.colour()+'-'
        plt.plot(x,y,col)


def openAndReadData (filename):
    #returns data from file in as numpy arrays in a list. One array for each run
    # In the arrays the data is ordered as [[cooling times],[cuvette temps],[platetemps],[runrfreq]]
    #run freq = 'Cal' for calibration runs
    with open(filename,'rU') as csvfile:
        file = csv.reader(csvfile)
        data = []
        Currentrun = 0
        rundata = [[],[],[]]
        for row in file:
            try :
                runnumber = int(row[5])
                if runnumber == Currentrun:
                    rundata[0].append(float(row[0])) #Times
                    rundata[1].append(ast.literal_eval(row[1])) # Cuvette Temp
                    rundata[2].append(ast.literal_eval((row[3]))) # Plate temp
                else:
                    rundata = np.array(rundata,dtype=object)
                    try:
                        dataset = Run(rundata,settemp= settemp, frequency = frequency, ambientgun=gun,ambientthermometer=ambient,timeofday=timeofday,day=investigation,runnumber=Currentrun)
                        data.append(dataset)
                    except: pass

                    Currentrun = runnumber
                    rundata = [[float(row[0])],[float(row[1])],[float(row[3])]]
                    gun = float(row[7])
                    ambient = float(row[8])
                    investigation = str(row[9])
                    timeofday = int(row[10])
                    settemp = float(row[2])
                    try:
                        frequency = float(row[6])
                    except ValueError:
                        frequency = row[6]
            except: pass
    return data


badruns = [16,17,21,25,29]

#for badrun in badruns:
 #   run = inv10[badrun-1]
  #  run.plotcooling()
def savedata():
    Alldata = openAndReadData('All Data2.csv')
    i=0
    for run in Alldata:
        astemp = run.asymptotictemp()
        print run,' asyptotic temp is',astemp,' and a freeze temp of',run.freezetemp
        if astemp == None:
            i += 1

    print 'number of fuck ups',i

    inv10 = [run for run in Alldata if run.day == '10']
    inv11b = [run for run in Alldata if run.day == '11b']
    inv12 = [run for run in Alldata if run.day == '12']
    investigations = [inv10,inv11b,inv12]

    pkl.dump(Alldata,open("processeddata.p","w"))

#savedata()