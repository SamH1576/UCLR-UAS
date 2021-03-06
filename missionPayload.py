import math
import GPSDistanceConvertor
import time
import threading

##Payload Parameters
global p_mass, g, dropped
p_mass = 0.2
g = 9.81

def startMission(VecCon, dataLAT, dataLONG, payloadDeployed, q_lock, scrQueue):
    with q_lock:
        scrQueue.put(['EntryStatus','Mission starting'])
    missThread = threading.Thread(target=missionThread, args=(VecCon, dataLAT, dataLONG, payloadDeployed, q_lock, scrQueue,))
    missThread.setDaemon(True) #ie when the module exits: kill thread
    missThread.start()
    with q_lock:
        scrQueue.put(['EntryStatus','Mission started'])

def missionThread(VecCon, dataLAT, dataLONG, payloadDeployed, q_lock, scrQueue):
    while(payloadDeployed.isSet() == False):
        VecCon.getGPSdata()
        currLAT = VecCon.MAVData['LAT']
        currLONG = VecCon.MAVData['LONG']
        targetLAT = dataLAT
        targetLONG = dataLONG
        dist2target = GPSDistanceConvertor.GPSXY(currLAT,currLONG,targetLAT,targetLONG)
        with q_lock:
            #scrQueue.put(['EntryX1',format(dist2target[0],'.4f')])
            #scrQueue.put(['EntryY1',format(dist2target[1],'.4f')])
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
    if(vel > 0):
        return(hypdist/vel)
    else:
        return 0.1

def boolDrop(alt, hypdist, vel):
    if(time2fall(alt)>(time2target(hypdist,vel))):
        return True
    else:
        return False


if __name__ == '__main__':
    import MAVComms
    import RPi.GPIO as GPIO

    def startMAVComms():
        NewConnection = MAVComms.MAVconnect('/dev/ttyACM0')
        #NewConnection = MAVComms.MAVconnect('udp:0.0.0.0:15440') 
        while(NewConnection.Connecting):
        #waiting to finish connecting
            pass
        
        if(NewConnection.ConnErrFlag != True):
            return NewConnection
        else:
            return None

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    pwm = GPIO.PWM(18, 100)
    pwm.start(5)

    dataLAT = 51.522198
    dataLONG = -0.2423644
    VecCon = startMAVComms()
    dropped = False
    while(dropped == False):
        VecCon.getGPSdata()
        currLAT = VecCon.MAVData['LAT']
        currLONG = VecCon.MAVData['LONG']
        targetLAT = dataLAT
        targetLONG = dataLONG
        dist2target = GPSDistanceConvertor.GPSXY(currLAT,currLONG,targetLAT,targetLONG)
        print format(dist2target[2],'.4f')
        if(boolDrop(VecCon.MAVData['ALT'],dist2target[2],VecCon.MAVData['GSPD'])):
	    pwm.ChangeDutyCycle(12.5)	    
            dropped = True
	    time.sleep(1)
            GPSdropLocation = currLAT, currLONG
        else:
            time.sleep(0.5)
            pass
    print('-----------')
    print('Payload Deployed')
    print GPSdropLocation
    VecCon.disconnectMAV()
    VecCon = None
