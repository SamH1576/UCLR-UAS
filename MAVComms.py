import time
from dronekit import connect, VehicleMode

class MAVconnect:
    def __init__(self, strCon):
        self.ConnectionString = strCon
	#dictionary of MAV data, can be extended if more info is needed
	self.MAVData = {'LAT': None, 'LONG': None, 'ALT': None, 'GSPD': None}
        self.ConnErrFlag = False
        try:
            self.vehicle = connect(self.ConnectionString, heartbeat_timeout=20, wait_ready=True)
        except:
            print('Connection timed out')
            self.ConnErrFlag = True
                     
    def getGPSdata(self):
        self.MAVData['LAT'] = self.vehicle.location.global_relative_frame.lat
        self.MAVData['LONG'] = self.vehicle.location.global_relative_frame.lon
        self.MAVData['ALT'] = self.vehicle.location.global_relative_frame.alt
        self.MAVData['GSPD'] = self.vehicle.groundspeed

    def disconnectMAV(self):
        self.vehicle.close
        print 'MAV disconnected'
