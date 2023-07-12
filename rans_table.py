# pip install tabulate

import re
from tabulate import tabulate

LogFile = "/var/log/zerto/zvr/zvm/logfile.csv"
Volumes = {}

def updateVolStat():
    file1 = open(LogFile, 'r')
    
    while True:
        # Get next line from file
        line = file1.readline()
    
        # if line is empty
        # end of file is reached
        if not line:
            break

        if("AlgoIdentificationEngine,PrintPeriodicLog" in line and "Training" in line):
            m = re.search("<(.*)> Training=(.*), AVG=(\d*)", line)
            volId = m.group(1)
            # alg = m.group(2)
            training = m.group(2).split(".",1)[0]
            avg = m.group(3).split(".",1)[0]
            Volumes[volId] = {"desc" : "Vol {} is in training period. {} left for training. Current AVG encryption ratio = {}".format(volId,training,avg),
                              "training" : training,
                              "avg" : avg,
                              "cusum" : 0}
        if("AlgoIdentificationEngine,PrintPeriodicLog" in line and not "Training" in line):
            m = re.search("<(.*)> AVG=(.*), CUSUM=(\d*)", line)
            if m is None:
                print(line)
            volId = m.group(1)
            # alg = m.group(2)
            avg = m.group(2).split(".",1)[0]
            cusum = m.group(3).split(".",1)[0]

            Volumes[volId] = {"desc" : "",
                              "training" : "",
                              "avg" : avg,
                              "cusum" : cusum}
    
    file1.close()

def printVolStatTable():
    col_names = ["Volume_Algorithm", "Training remaining" , "AVG encryption" , "change in trend"]

    data = map(lambda kv: [kv[0], kv[1]["training"], kv[1]["avg"], kv[1]["cusum"]], Volumes.items())
  
    #display table
    print(tabulate(data, headers=col_names))

updateVolStat()
printVolStatTable()
