import time
from dronekit import connect
import threading

class MAVconnect:
    def __init__(self, strCon):
        self.ConnectionString = strCon
	self.vehicle = None
	#dictionary of MAV data, can be extended if more info is needed
        self.MAVData = {'LAT': None, 'LONG': None, 'ALT': None, 'GSPD': None, 'ROLL': None, 'PITCH': None, 'YAW': None}
        self.ConnErrFlag = False
        self.Connecting = False
        self.startConnThread()

    def startConnThread(self):  
        connectThread = threading.Thread(name= 'connectThread', target=self.connectVehicle)
        connectThread.setDaemon(True) #ie when the module exits: kill thread
        connectThread.start()
        #wait for thread to return
        connectThread.join()

    def connectVehicle(self):
        self.Connecting = True
        try:
            self.vehicle = connect(self.ConnectionString, wait_ready=True)
            self.Connecting = False
        except:
            print('Connection timed out')
            self.Connecting = False
            self.ConnErrFlag = True
               
    def getGPSdata(self):
        self.MAVData['LAT'] = self.vehicle.location.global_relative_frame.lat
        self.MAVData['LONG'] = self.vehicle.location.global_relative_frame.lon
        self.MAVData['ALT'] = self.vehicle.location.global_relative_frame.alt
        self.MAVData['GSPD'] = self.vehicle.groundspeed

    def getLocalPos(self):
        self.MAVData['NORTH'] = self.vehicle.location.local_frame.north
        self.MAVData['EAST'] = self.vehicle.location.local_frame.east
        self.MAVData['DOWN'] = self.vehicle.location.local_frame.down

    def getAttitude(self):
        self.MAVData['ROLL'] = self.vehicle.attitude.roll
        self.MAVData['PITCH'] = self.vehicle.attitude.pitch
        self.MAVData['YAW'] = self.vehicle.attitude.yaw

    def armVehicle(self):
        print('this is ONLY for testing local frame')
        self.vehicle.armed = True
        print('Armed: %s' % self.vehicle.armed)

    def disconnectMAV(self):
        print 'called'
        self.vehicle.close()
        print 'MAV disconnected'

if __name__ == '__main__':
#	m = MAVconnect('/dev/ttyAMA0')
	m = MAVconnect('/dev/ttyACM0')
#	m = MAVconnect('/dev/serial0,57600')
#	m.armVehicle()
#	time.sleep(2)
	
	import IRS

        print('Starting MAV connection')
        if(m.vehicle is not None):
                print('Initialising mission object')
                mission = IRS.missionRecon(m)
        	print('Starting detection')
	        mission.detection()
        else:
                print('No connection, exiting')


