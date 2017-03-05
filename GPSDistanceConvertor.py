import time
import math
import numpy

def GPSXY(lat1, long1, lat2, long2):
    #worth noting lat1 long1 is location, lat2 long2 is target
    MAJ = 6356752.3142
    MINR = 6378137

    dLat = lat2 - lat1
    dLon = long2 - long1

    long1, lat1, long2, lat2 = map(math.radians, [long1, lat1, long2, lat2]) 

    truA1 = math.atan((MAJ**2)/(MINR**2)*math.tan(lat1))
    truA2 = math.atan((MAJ**2)/(MINR**2)*math.tan(lat2))

    rad1 = ( 1/((math.cos(truA1))**2/MINR**2 + (math.sin(truA1))**2/MAJ**2))**0.5
    rad2 = ( 1/((math.cos(truA2))**2/MINR**2 + (math.sin(truA2))**2/MAJ**2))**0.5

    xyEarth1a = rad1*math.cos(truA1)# %B9
    xyEarth1b = rad2*math.cos(truA2)# %B10
    xyEarth2a = rad1*math.sin(truA1)# %B11
    xyEarth2b = rad2*math.sin(truA2)# %B12
 
    Y =((xyEarth1a-xyEarth1b)**2+(xyEarth2a-xyEarth2b)**2)**0.5
    X = 2*math.pi*((((xyEarth1a+xyEarth1b)/2))/(2*math.pi))*(long2-long1)
    
    if dLat<0: #%%When in N Hemisphere, this means going South (-Y) 
        Y = -(math.fabs(Y));
    else:
        Y = math.fabs(Y);
    

    if dLon<0: #%% This means going West (-X) 
        X = -(math.fabs(X));
    else:
        X = math.fabs(X);
    
    TOTAL =((X)**2+(Y)**2)**0.5

    return(X,Y,TOTAL)

def addXY2GPS(lat_in, long_in, X, Y):
    R= 6378137.0
    dLat = Y/R
    dLon = X/(R*math.cos(math.pi*lat_in/180))
    lat_o = lat_in + dLat * 180/math.pi
    long_o = long_in + dLon * 180/math.pi
    return(lat_o, long_o)

def BearingMeet(x1,y1,x2,y2,bearing1,bearing2):
    if(bearing1 == bearing2):
        print("Bearings are identical")
        return None,None
    if((numpy.fabs(bearing1-bearing2))==180):
        print('bearings are parallel')
        return None,None

    if(numpy.fabs(bearing1-bearing2) < 5 ):
    	print("Bearings too close")
    	return None,None
    
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
	print(Xout, Yout)
    else:
        if(bearing1 == 0):
            Xout = x1
            Yout = (y2*numpy.tan(theta2) - y1*numpy.tan(theta1) + x1 - x2)/(numpy.tan(theta2) - numpy.tan(theta1))
        if(bearing2 == 0):
            Xout = x2
            Yout = (y2*numpy.tan(theta2) - y1*numpy.tan(theta1) + x1 - x2)/(numpy.tan(theta2) - numpy.tan(theta1))

    if(Xout>0 and East == False):
        print("These bearings do not converge")
        return(None, None)
    if(Yout>0 and South == True):
        print("These bearings do not converge")
        return(None, None)
    
    return(Xout, Yout)


##For validation - matches MATLAB script
##X,Y,TOTAL = GPSXY(45.4649135,-95.9090323,45.46555306,-95.9097683)
##print(X)
##print(Y)
##print(TOTAL)
