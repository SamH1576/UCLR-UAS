import time
from dronekit import connect, VehicleMode
import threading

class MAVconnect:
    def __init__(self, strCon):
        self.ConnectionString = strCon
	#dictionary of MAV data, can be extended if more info is needed
        self.MAVData = {'LAT': None, 'LONG': None, 'ALT': None, 'GSPD': None}
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
            self.vehicle = connect(self.ConnectionString, heartbeat_timeout=20, wait_ready=True)
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

    def disconnectMAV(self):
        print 'called'
        self.vehicle.close()
        print 'MAV disconnected'
