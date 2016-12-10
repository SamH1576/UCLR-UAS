import time
import math

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

##For validation - matches MATLAB script
##X,Y,TOTAL = GPSXY(45.4649135,-95.9090323,45.46555306,-95.9097683)
##print(X)
##print(Y)
##print(TOTAL)
