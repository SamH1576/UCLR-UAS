#from IRS import missionRecon
import csv


with open('SampleGPSBearingData.csv', 'rb') as f:
    reader = csv.reader(f)
    your_list = list(reader)

posData = {}
i = 0
posData['target' + str(i)] = {}
posData['target' + str(i)]['LAT'] = {}
posData['target' + str(i)]['LONG'] = {}
posData['target' + str(i)]['HEADING'] = {}

for x in range(len(your_list)):
	if(x == 0):
		pass
	else:
	    posData['target' + str(i)]['LAT'][x] = your_list[x][1]
	    posData['target' + str(i)]['LONG'][x] = your_list[x][0]
	    posData['target' + str(i)]['HEADING'][x] =  your_list[x][2]

m = missionRecon(None)
avg_lat, avg_long = m.calculation(self, posData, str(i))
