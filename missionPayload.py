import math
import GPSDistanceConvertor

##Payload Parameters
global p_mass, g, dropped
p_mass = 1
g = 9.81
dropped = False 

def startMission(VecCon, Target):
    while(dropped == False):
        VecCon.getGPSdata()
        currLAT = VecCon.MAVData['LAT']
        currLONG = VecCon.MAVData['LONG']
        targetLAT = Target[0]
        targetLONG = Target[1]
        dist2target = GPSDistanceConvertor.GPSXY(currLAT,currLONG,targetLAT,targetLONG)
        if(boolDrop(VecCon.MAVData['ALT'],dist2target[2],VecCon.MAVData['GSPD'])):
            dropped = True
        else:
            dropped = False
        
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
       print('Dropped')
