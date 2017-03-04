# class testclass:
# 	def run(self):
# 		posData = {}
# 		for i in range(4):
# 			posData['target'+str(i)] = {}
# 			for j in range(10):
# 				posData['target'+str(i)][j] = j

# 		return posData

# t = testclass()
# data = t.run()

# for key, value in data['target0'].iteritems():
# 	print key, value

# print len(data)

# testMatrix = []
# for i in range(10):
# 	if(i == 3):
# 		testMatrix.append([])
# 		testMatrix[i].append(0)
# 		testMatrix[i].append(0)
# 	else:	
# 		testMatrix.append([])
# 		testMatrix[i].append(1)
# 		testMatrix[i].append(2)
# print testMatrix


xyMatrix = []   
data = 0
for i in range(10):
	for j in range(10):
		if(i == j or i == 0):
			#REMEMBER TO STRIP ZEROS
			xyMatrix.append([])
			xyMatrix[data].append(0)
			xyMatrix[data].append(0)
		else:
			xyMatrix.append([])
			xyMatrix[data].append(1)
			xyMatrix[data].append(2)
		data += 1

print xyMatrix

# with open('log.txt', 'w') as f:
# 	for key, value in data.items():
# 		f.write('%s:%s\n' % (key, value))
