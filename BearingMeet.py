import numpy
#from collections import deque

class estiPosition:
    def __init__(self, VecConn):
        #declare array here so it can be accessed external as part of the class.
        self.arrPos = []
        #add second dimension ie y
        #NOTE to add to this array:
        #first -> arrPos.append([]) adds another row
        #then arrPos[i].append("foo") adds item "foo" in arrPos[i][0]
        #e.arrPos[i].append("bar") adds item "bar" in arrPos[i][1]

        #connection which is passed to the class
        self.MAVcomms = VecConn

    def main(self):
        print 'Start Position Estimation'
        dataCollectionActive = True

        #collect data points
        while dataCollectionActive = True:
            #get current position
            currPos = self.MAVcomms.getGPSdata()
            currAtt = self.MAVcomms.getAttitude()
            
            #check vehicle attitude (if turning don't try and get a reading) dx/dt or dy/dt > 1
            if(abs(self.MAVcomms.MAVData['ROLL'])<0.175 and abs(self.MAVcomms.MAVData['PITCH'])<0.175)
            #check camera - is target sighted and centred?
            #if yes record current GPS positon, camera servo position and heading (vehicle.heading)
            
        #if there are two readings, compare reading 1 to reading 2 (Or 1-2, 1-3, 1-4 etc for good average?)
        #record estimate GPS pposition of target
        
        #when there are enough [?] recordings, remove outliers and average
        #report this back although with the character (TBA - sent through MAVLink or by 3g?)
        
    def BearingMeet(self,x1,y1,x2,y2,bearing1,bearing2):
        if(bearing1 == bearing2):
            print("Bearings are identical")
            return None
        if((numpy.fabs(bearing1-bearing2))==180):
            print('bearings are parallel')
            return None
        
        theta1 = numpy.radians(bearing1)
        theta2 = numpy.radians(bearing2)
        
        if(bearing1>=90 and bearing1<=270):
            #bearing pointing south, Yout cannot be above 0
            South = True
        else:
            South = False

        if(bearing1>0 and bearing1<180):
            #pointing East, so Xout cannot be less than 0
            East = True
        else:
            East = False
        #a special case is when bearing1 or bearing2 equals 0, in which case Xout will equal x1 or x2 depending on which bearing is 0
        if(bearing1 != 0 and bearing2 != 0):      
            Xout = ((x2*(1/numpy.tan(theta2))) - (x1*(1/numpy.tan(theta1))) + y1 - y2)/((1/numpy.tan(theta2)) - (1/numpy.tan(theta1)))
            Yout = (y2*numpy.tan(theta2) - y1*numpy.tan(theta1) + x1 - x2)/(numpy.tan(theta2) - numpy.tan(theta1))
        else:
            if(bearing1 == 0):
                Xout = x1
                Yout = (y2*numpy.tan(theta2) - y1*numpy.tan(theta1) + x1 - x2)/(numpy.tan(theta2) - numpy.tan(theta1))
            if(bearing2 == 0):
                Xout = x2
                Yout = (y2*numpy.tan(theta2) - y1*numpy.tan(theta1) + x1 - x2)/(numpy.tan(theta2) - numpy.tan(theta1))

        if(Xout>0 and East == False):
            print("These bearings do not converge")
            return None
        if(Yout>0 and South == True):
            print("These bearings do not converge")
            return None
        
        return(Xout, Yout)


##testing class

##e = estiPosition("Doris")
##for i in range(10):
##    e.arrPos.append([])
##    e.arrPos[i].append(1)
##    e.arrPos[i].append(2)
##
##for j in range(len(e.arrPos)):
##    print e.arrPos[j][0]
##    print e.arrPos[j][1]

###Used to test the function    
#----------
##x1 = 0
##y1 = 0
##x2 = -2
##y2 = 2
##
##bearing1 = 290
##bearing2 = 0
##
##e = estiPosition("test")
##res = e.BearingMeet(x1,y1,x2,y2,bearing1,bearing2)
##if(res != None):
##    print(numpy.round(float(res[0]),decimals=3))
##    print(numpy.round(float(res[1]),decimals=3))
##


## used for testing
##    if((x2-x1)>0):
##        if((y2-y1)>0):
##            quadrant = 1
##        else:
##            quadrant = 2
##    else:
##        if((y2-y1)>0):
##            quadrant = 4
##        else:
##            quadrant = 3
##
##    print quadrant

#-------------------------------------------
#below is original attempt using linalg rather than geometry
#
##    if((numpy.fabs(bearing1-bearing2))==180):
##        print('bearings are parallel')
##
##    if((bearing2-bearing1) > 90):
##        print 'bearings do not converge'
##        return 0
##    
##    ##convert bearings into radians and change rotate them 90deg
##    theta1 = numpy.pi/2 - numpy.radians(bearing1)
##    theta2 = numpy.pi/2 - numpy.radians(bearing2)
##    
##    m1 = numpy.tan(theta1)
##    m2 = numpy.tan(theta2)   
##    C1 = y1 - m1*x1
##    C2 = y2 - m2*x2
##
##    a = numpy.array([[-m1,1],[-m2,1]])
##    b = numpy.array([[C1],[C2]])
##
##    try:
##        #return an array of X, Y coords of bearing meeting point
##        return(numpy.linalg.solve(a,b))    
##    except numpy.linalg.LinAlgError:
##        print 'Error: Bearings are identical'

##    
