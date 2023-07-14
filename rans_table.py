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
            if volId not in Volumes:
                Volumes[volId] = {}
            Volumes[volId].update({"desc" : "Vol {} is in training period. {} left for training. Current AVG encryption ratio = {}".format(volId,training,avg),
                                   "training" : training,
                                   "avg" : avg,
                                   "cusum" : 0})
            
        if("AlgoIdentificationEngine,PrintPeriodicLog" in line and not "Training" in line):
            m = re.search("<(.*)> AVG=(.*), CUSUM=(-?\d*)", line)
            if m is None:
                print(line)
            volId = m.group(1)
            # alg = m.group(2)
            avg = m.group(2).split(".",1)[0]
            cusum = m.group(3).split(".",1)[0]
            if volId not in Volumes:
                Volumes[volId] = {}
            Volumes[volId].update({"desc" : "",
                                   "training" : "",
                                   "avg" : avg,
                                   "cusum" : cusum})
                       
        if("VraDataAccessor" in line and "Got VolumeMetrics." in line):
            for m in re.finditer(" (\d+) => CU_SUM => EncryptedBlocksCounter = (\d+), UnencryptedBlocksCounter = (\d+), AVG_ENTROPY => EncryptedBlocksCounter = (\d+), UnencryptedBlocksCounter = (\d+) ", line):
                volId = m.group(1)
                cuSumEnc = int(m.group(2))
                cuSumUnEnc = int(m.group(3))
                entEnc = int(m.group(4))
                entUnEnc = int(m.group(5))
                
                addAlgStatsToVol(volId+"_CU_SUM", cuSumEnc, cuSumUnEnc)
                addAlgStatsToVol(volId+"_AVG_ENTROPY", entEnc, entUnEnc)        

    file1.close()

def addAlgStatsToVol(volAlg, enc, unEnc):
    if volAlg not in Volumes:
        Volumes[volAlg] = {}
        diffEnc = 0
        diffUnEnc = 0
    else:
        diffEnc = enc - Volumes[volAlg]["enc"]
        diffUnEnc = unEnc - Volumes[volAlg]["unEnc"]

    Volumes[volAlg].update({"enc" : enc,
                            "unEnc": enc,
                            "cur": 100 * diffEnc / (diffEnc + diffUnEnc) if diffEnc + diffUnEnc > 0 else "NA",
                            "total": enc + unEnc})

def printVolStatTable():
    col_names = ["Volume_Algorithm", "Training\nremaining" , "AVG\nencryption\nratio" , "change\nin trend", "cur\nencryption\nratio", "total\nblocks\nprocessed"]

    data = map(lambda kv:                
                [ kv[0], kv[1]["training"]  if "training" in kv[1] else "NA", 
                 kv[1]["avg"] if "avg" in kv[1] else "NA", 
                 kv[1]["cusum"] if "cusum" in kv[1] else "NA", 
                kv[1]["cur"] if "cur" in kv[1] else "NA",
                kv[1]["total"] if "total" in kv[1] else "NA"], 
               Volumes.items())
  
    #display table
    print(tabulate(data, headers=col_names))

updateVolStat()
printVolStatTable()
