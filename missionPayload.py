import math
import GPSDistanceConvertor
import time
import threading

##Payload Parameters
global p_mass, g, dropped
p_mass = 1
g = 9.81

def startMission(VecCon, Target, payloadDeployed, q_lock, scrQueue):
    with q_lock:
        scrQueue.put(['EntryStatus','Mission starting'])
    missThread = threading.Thread(target=missionThread, args=(VecCon, Target, payloadDeployed, q_lock, scrQueue,))
    missThread.setDaemon(True) #ie when the module exits: kill thread
    missThread.start()
    with q_lock:
        scrQueue.put(['EntryStatus','Mission started'])

def missionThread(VecCon, Target, payloadDeployed, q_lock, scrQueue):
    while(payloadDeployed.isSet() == False):
        VecCon.getGPSdata()
        currLAT = VecCon.MAVData['LAT']
        currLONG = VecCon.MAVData['LONG']
        targetLAT = Target[0]
        targetLONG = Target[1]
        dist2target = GPSDistanceConvertor.GPSXY(currLAT,currLONG,targetLAT,targetLONG)
        with q_lock:
            scrQueue.put(['EntryX1',format(dist2target[0],'.4f')])
            scrQueue.put(['EntryY1',format(dist2target[1],'.4f')])
            scrQueue.put(['EntryTotal1',format(dist2target[2],'.4f')])
        if(boolDrop(VecCon.MAVData['ALT'],dist2target[2],VecCon.MAVData['GSPD'])):
            payloadDeployed.set()
        else:
            time.sleep(0.5)
            pass
    with q_lock:
        scrQueue.put(['EntryStatus','Mission exiting'])
    VecCon.disconnectMAV()
    VecCon = None
        
def time2fall(alt):
    if(alt > 0):
        return(math.sqrt((2*alt)/g))
    else:
        return 0.1
    
def time2target(hypdist, vel):
    if(vel != 0):
        return(hypdist/vel)
    else:
        return 0.1

def boolDrop(alt, hypdist, vel):
    if(time2fall(alt)>(time2target(hypdist,vel))):
        return True
    else:
        return False
