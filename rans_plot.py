# pip install plotext

import re
import sys
import time
from datetime import datetime
import plotext as plt

LogFile = "/var/log/zerto/zvr/zvm/logfile.csv"

if len(sys.argv) < 2:
    print("Usage: {} <volId>".format(sys.argv[0]))
    print("You can get the `volId` by runing 'rans_table.py' and copying the volume you are interested in")
    sys.exit(1)

volId = sys.argv[1]

dataArr = []
lastTime = None

def updateVolStat():
    global lastTime
    file1 = open(LogFile, 'r')
    
    while True:
        # Get next line from file
        line = file1.readline()

        if not line:
            break

        if("AlgoIdentificationEngine,PrintPeriodicLog" in line and volId in line):
            m = re.search(",(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{2}).*,I,.*AVG=(\d*).*, CUSUM=(-?\d*)", line)
            if m is None:
                print(line)

            timeStr = m.group(1)
            time = datetime.strptime(timeStr, "%Y-%m-%d %H:%M:%S.%f")
            avg = int(m.group(2))
            cusum = int(m.group(3))

            if lastTime is None:
                lastTime = time
            elif lastTime > time:
                continue

            lastTime = time
            
            dataArr.append([time, avg, cusum])
            if(len(dataArr) > 30):
                dataArr.pop(0)

    file1.close()


def plotStats():
    xArr = [subarray[0].strftime("%H:%M:%S") for subarray in dataArr] # .strftime("%H:%M:%S")
    avgArr = [subarray[1] for subarray in dataArr]
    cusumArr = [subarray[2] for subarray in dataArr]
    print(xArr)
    print(avgArr)
    print(cusumArr)
    
    #plt.date_form(' H:M:S')
    #strxArr = plt.datetimes_to_string(xArr)
    
    plt.plot(avgArr, yside = "left", label = "enc ratio (left Axis)", marker = "R")
    plt.plot(cusumArr, yside = "right", label = "change in trend (right Axis)", marker = "T")
    plt.show()

while(True):
    updateVolStat()
    plotStats()
    time.sleep(10)
