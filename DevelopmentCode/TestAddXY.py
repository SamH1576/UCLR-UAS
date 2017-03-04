from GPSDistanceConvertor import addXY2GPS

lat1 = 45.4649135
long1 = -95.9090323
X = -56.22
Y = 70.7

result1, result2 = addXY2GPS(lat1, long1, X, Y)
print lat1, long1
print ("%.7f" % result1, "%.7f" % result2)