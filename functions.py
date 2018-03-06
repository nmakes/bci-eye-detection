def getData(rawLines):

	readingMeta = True
	data = {'relation':'unnamed_relation', 'attributes':[], 'data':[]}

	for line in rawLines:

		if readingMeta:
			words = line.split()

			if len(words) <= 0:
				continue
			elif words[0] == '@RELATION':
				data['relation'] = words[1]

			elif words[0] == '@ATTRIBUTE':
				data['attributes'].append(words[1])

			elif words[0] == '@DATA':
				readingMeta = False

			else:
				continue

		else:

			contents = line.split(',')
			
			for (i,c) in enumerate(contents):
				contents[i] = float(c)
			
			data['data'].append(contents)

	return data


def getField(data, field):

	# get only a specific attribute from the whole data
	vals = []
	pos = data['attributes'].index(field)

	for d in data['data']:
		vals.append(d[pos])

	return vals


def suppressOutliers1D(x, threshold, mode='mean'):

	X = x
	M = np.max(X)

	print X
	print M

	val = 0

	if mode=='mean':
		val = np.mean(x)

	X[X>threshold*M] = val
	X[X<-threshold*M] = val

	return X