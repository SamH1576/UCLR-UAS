class testclass:
	def run(self):
		posData = {}
		for i in range(4):
			posData['target'+str(i)] = {}
			for j in range(10):
				posData['target'+str(i)][j] = j

		return posData

t = testclass()
data = t.run()

for key, value in data['target0'].iteritems():
	print key, value

print len(data)

testMatrix = []
testMatrix.append([])
testMatrix[0].append(1)
testMatrix[0].append(2)
print testMatrix[0][1]


with open('log.txt', 'w') as f:
	for key, value in data.items():
		f.write('%s:%s\n' % (key, value))
