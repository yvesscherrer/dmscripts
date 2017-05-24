#! /usr/bin/python3
# -*- coding: utf-8 -*-

import numpy, csv, math, random, os, subprocess


inputencoding = 'utf-8-sig'
inputdelimiter = ','
outputencoding = 'utf-8-sig'
outputdelimiter = ','
rugpath = "/home/yvessche/RuG-L04/bin/"
rugencoding = "iso-8859-1"


############## Input/Output ##############


def loadDataMatrix(dataMatrixName):
	print("Loading data matrix from file", dataMatrixName)
	columnheaders = []
	data = {}
	rd = csv.reader(open(dataMatrixName, 'r', encoding=inputencoding), delimiter=inputdelimiter)
	first = True
	for line in rd:
		if first:
			columnheaders = line[1:]
			first = False
			continue
		data[line[0]] = []
		for v in line[1:]:
			if v == "":
				data[line[0]].append(set())
			else:
				data[line[0]].append(set(v.split("|")))
	return ([data[x] for x in sorted(data.keys())], columnheaders, sorted(data.keys()))


def loadPercentDataMatrix(dataMatrixName):
	print("Loading percent data matrix from file", dataMatrixName)
	columnheaders = []
	data = {}
	rd = csv.reader(open(dataMatrixName, 'r', encoding=inputencoding), delimiter=inputdelimiter)
	first = True
	for line in rd:
		if first:
			variables = [x.split("_")[0] for x in line[1:]]
			variants = [x.split("_")[1] for x in line[1:]]
			first = False
			continue
		data[line[0]] = []
		previousVariable = ""
		for i, value in enumerate(line[1:]):
			variable = variables[i]
			variant = variants[i]
			if variable != previousVariable:
				data[line[0]].append({})
				previousVariable = variable
			data[line[0]][-1][variant] = float(value)
	uniqueVariables = [x for i, x in enumerate(variables) if i == 0 or variables[i-1] != x]
	return ([data[x] for x in sorted(data.keys())], uniqueVariables, sorted(data.keys()))


def loadSimilarityMatrix(simMatrixName):
	print("Loading similarity matrix from file", simMatrixName)
	columnheaders = []
	rd = csv.reader(open(simMatrixName, 'r', encoding=inputencoding), delimiter=inputdelimiter)
	first = True
	i = 0
	for line in rd:
		if first:
			columnHeaders = line[1:]
			simMatrix = numpy.zeros((len(columnHeaders), len(columnHeaders)))
			first = False
			continue
		simMatrix[i] = [float(x) for x in line[1:]]
		i += 1
	return (simMatrix, columnHeaders)


def loadParamMatrix(matrixName):
	print("Loading parameter matrix from file", matrixName)
	rd = csv.reader(open(matrixName, 'r', encoding=inputencoding), delimiter=inputdelimiter)
	first = True
	values = {}
	for line in rd:
		if first:
			valueIndex = line.index("VALUE")
			if valueIndex < 0:
				return None
			first = False
		else:
			values[line[0]] = float(line[valueIndex])
	return values


def writeMatrix(matrix, matrixName, rowHeaders=None, columnHeaders=None):
	print("Writing result matrix to file", matrixName)
	f = open(matrixName, 'w', encoding=outputencoding)
	wr = csv.writer(f, delimiter=outputdelimiter)
	if columnHeaders:
		wr.writerow(["LOC"] + columnHeaders)
	for i in range(matrix.shape[0]):
		r = []
		if rowHeaders:
			r.append(rowHeaders[i])
		if len(matrix.shape) > 1:
			r.extend(matrix[i])
		else:
			r.append(matrix[i])
		wr.writerow(r)
	f.close()
	print("Done")


def invertMatrix(matrix):
	return 1 - matrix


def countMultipleAnswers(dataMatrix):
	nbPart = 0
	sumMulti = 0
	for row in dataMatrix:
		nbAnswers = 0
		nbMulti = 0
		for column in row:
			if len(column) > 0:
				nbAnswers += 1
			if len(column) > 1:
				nbMulti += 1
		nbPart += 1
		sumMulti += (nbMulti / nbAnswers)
	return sumMulti / nbPart


############## Similarity matrix creation ##############


# for dict data (numerical)
def EuclidRIW(a, b):
	sim = 0.0
	nbComp = 0
	for i in range(len(a)):
		variablesum = 0.0
		for key in set(a[i].keys()) | set(b[i].keys()):
			variablesum += (a[i].get(key, 0.0) - b[i].get(key, 0.0)) ** 2
		sim += (1.0 - math.sqrt(variablesum))
		nbComp += 1
	return sim / nbComp


# for dict data (numerical)
def Euclid(a, b):
	varsum = 0.0
	nbcomp = 0
	for i in range(len(a)):
		for key in set(a[i].keys()) | set(b[i].keys()):
			varsum += (a[i].get(key, 0.0) - b[i].get(key, 0.0)) ** 2
			nbcomp += 1
	sim = 1.0 - math.sqrt(varsum/nbcomp)
	return sim


# for set data
def JaccardRIW(a, b):
	sim = 0.0
	nbComp = 0
	for i in range(len(a)):
		if (len(a[i]) == 0) or (len(b[i]) == 0):	# missing value in one field
			continue
		sim += len(a[i] & b[i]) / len(a[i] | b[i])
		nbComp += 1
	return sim / nbComp


def DiceRIW(a, b):
	sim = 0
	nbComp = 0
	for i in range(len(a)):
		if (len(a[i]) == 0) or (len(b[i]) == 0):	# missing value in one field
			continue
		sim += 2 * len(a[i] & b[i]) / (len(a[i]) + len(b[i]))
		nbComp += 1
	return sim / nbComp


def OverlapRIW(a, b):
	sim = 0
	nbComp = 0
	for i in range(len(a)):
		if (len(a[i]) == 0) or (len(b[i]) == 0):	# missing value in one field
			continue
		sim += len(a[i] & b[i]) / min(len(a[i]), len(b[i]))
		nbComp += 1
	return sim / nbComp


def RIW(a, b):
	sim = 0
	nbComp = 0
	for i in range(len(a)):
		if (len(a[i]) == 0) or (len(b[i]) == 0):	# missing value in one field
			continue
		if a[i] == b[i]:
			sim += 1
		nbComp += 1
	return sim / nbComp


def RandomRIW(a, b):
	sim = 0
	nbComp = 0
	for i in range(len(a)):
		if (len(a[i]) == 0) or (len(b[i]) == 0):	# missing value in one field
			continue
		if len(a[i]) == 1:
			ax = list(a[i])[0]
		else:
			ax = random.choice(list(a[i]))
		if len(b[i]) == 1:
			bx = list(b[i])[0]
		else:
			bx = random.choice(list(b[i]))
		if ax == bx:
			sim += 1
		nbComp += 1
	return sim/nbComp


def Hamming(a, b, variants):
	sim = 0
	nbComp = 0
	for i in range(len(a)):
		if (len(a[i]) == 0) or (len(b[i]) == 0):	# missing value in one field
			continue
		for v in variants[i]:
			if (v in a[i]) and (v in b[i]):
				sim += 1
			elif not(v in a[i]) and not(v in b[i]):
				sim += 1
			nbComp += 1
	return sim / nbComp


def computeSimilarityMatrix(dataMatrix, dataRowHeaders, simMetric):
	print("Compute similarity matrix with metric", simMetric)
	if simMetric == "Hamming":
		variants = []
		for i in range(len(dataRowHeaders)):
			for j in range(len(dataMatrix[i])):
				if len(variants) <= j:
					variants.append(set())
				variants[j] = variants[j].union(dataMatrix[i][j])

	simMatrix = numpy.zeros((len(dataRowHeaders), len(dataRowHeaders)))
	for i1 in range(len(dataRowHeaders)):
		for i2 in range(len(dataRowHeaders)):
			if i2 < i1:
				continue
			else:
				if simMetric == "Hamming":
					s = globals()[simMetric](dataMatrix[i1], dataMatrix[i2], variants)
				else:
					s = globals()[simMetric](dataMatrix[i1], dataMatrix[i2])
				simMatrix[i1, i2] = s
				simMatrix[i2, i1] = s
	return simMatrix


def filterSimilarityMatrix(simMatrix, simRows, keepRows):
	deleteRows = [i for i, value in enumerate(simRows) if value not in keepRows]
	#print(simMatrix.shape, len(simRows), len(deleteRows))
	simMatrix = numpy.delete(simMatrix, deleteRows, axis=0)
	simMatrix = numpy.delete(simMatrix, deleteRows, axis=1)
	simRows = [x for x in simRows if x in keepRows]
	#print(simMatrix.shape, len(simRows))
	return simMatrix, simRows


############## Parameter matrix creation ##############


def removeDiagonal(m):
	n = numpy.zeros((m.shape[0], m.shape[1]-1))
	for i in range(m.shape[0]):		# for each row
		n[i] = numpy.concatenate((m[i][:i], m[i][i+1:]), axis=0)
	return n


def computeParameterMatrix(simMatrix, parameterName):
	print("Compute parameter matrix for", parameterName)
	m = removeDiagonal(simMatrix)
	if parameterName == "max":
		return numpy.amax(m, axis=1)
	elif parameterName == "min":
		return numpy.amin(m, axis=1)
	elif parameterName == "mean":
		return numpy.mean(m, axis=1)
	elif parameterName == "stddev":
		return numpy.std(m, axis=1)
	elif parameterName == "skew":
		import scipy.stats
		return scipy.stats.skew(m, axis=1)
	else:
		print("Parameter {} unknown!".format(parameterName))
		return None

# needs testing
def computeCorrelationMatrix(simMatrix1, simMatrix2):
	print("Compute correlation matrix")
	m1 = removeDiagonal(simMatrix1)
	m2 = removeDiagonal(simMatrix2)
	n = numpy.zeros((m1.shape[0],))
	for i in range(m1.shape[0]):
		import scipy.stats
		n[i] = scipy.stats.stats.pearsonr(m1[i], m2[i])[0]
	return n


############## Clustering, MDS and local incoherence calculation using RuG/L04 ##############


def linc(simMatrix, geoDistMatrix, rows):
	distMatrix = invertMatrix(simMatrix)
	s = "{}\n".format(len(rows))
	for row in rows:
		s += "{}\n".format(row)
	for i, row in enumerate(distMatrix):
		for value in row[:i]:
			s += "{}\n".format(value)
	f = open("linc_temp1.txt", "w", encoding="utf8")
	f.write(s)
	f.close()

	t = "{}\n".format(len(rows))
	for row in rows:
		t += "{}\n".format(row)
	for i, row in enumerate(geoDistMatrix):
		for value in row[:i]:
			t += "{}\n".format(value)
	f = open("linc_temp2.txt", "w", encoding="utf8")
	f.write(t)
	f.close()

	print("Calling linc...")
	pipe = subprocess.Popen([rugpath + "linc", "-D", "linc_temp1.txt", "linc_temp2.txt"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
	pipeout, pipeerr = pipe.communicate()
	print(pipeerr.decode(rugencoding))
	if pipeout == "":
		print("stopping here")
		return None
	if "linc_temp1.txt" in os.listdir("."):
		os.remove("linc_temp1.txt")
	if "linc_temp2.txt" in os.listdir("."):
		os.remove("linc_temp2.txt")
	return float(pipeout.strip())


def cluster(simMatrix, rows, algorithm, numberClusters):
	distMatrix = invertMatrix(simMatrix)
	s = "{}\n".format(len(rows))
	for row in rows:
		s += "{}\n".format(row)
	for i, row in enumerate(distMatrix):
		for value in row[:i]:
			s += "{}\n".format(value)

	if algorithm in ("sl", "cl", "ga", "wa", "uc", "wc", "wm"):
		print("Calling cluster ({})...".format(algorithm))
		pipe = subprocess.Popen([rugpath + "cluster", "-" + algorithm], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
		clusterout, clustererr = pipe.communicate(s.encode(rugencoding))
		print(clustererr.decode(rugencoding))
		if clusterout == "":
			print("stopping here")
			return None

		print("Calling clgroup ({})...".format(numberClusters))
		pipe2 = subprocess.Popen([rugpath + "clgroup", "-n", str(numberClusters)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
		clgroupout, clgrouperr = pipe2.communicate(clusterout)
		print(clgrouperr.decode(rugencoding))
		if clgroupout == "":
			print("stopping here")
			return None

		result = clgroupout.decode(rugencoding)
		currentCluster = 0
		clusterAttributions = {}
		for line in result.split("\n"):
			line = line.strip()
			if line == "":
				currentCluster += 1
			else:
				clusterAttributions[line.strip()] = currentCluster

		n = numpy.zeros(len(rows),)
		for i, row in enumerate(rows):
			n[i] = clusterAttributions[row]
		return n


def mds(simMatrix, rows, dims):
	distMatrix = invertMatrix(simMatrix)
	s = "{}\n".format(len(rows))
	for row in rows:
		s += "{}\n".format(row)
	for i, row in enumerate(distMatrix):
		for value in row[:i]:
			s += "{}\n".format(value)

	print("Calling mds ({})...".format(dims))
	pipe = subprocess.Popen([rugpath + "mds", "-K", str(dims)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
	mdsout, mdserr = pipe.communicate(s.encode(rugencoding))
	print(mdserr.decode(rugencoding))
	if mdsout == "":
		print("stopping here")
		return None

	result = mdsout.decode(rugencoding)
	values = {}
	prevID = ""
	for line in result.split("\n"):
		line = line.strip()
		if line == str(dims):
			continue
		if line.startswith("#") or line == "":
			continue
		if prevID == "":
			prevID = line
			values[prevID] = []
		else:
			values[prevID].append(float(line))
		if len(values[prevID]) == dims:
			prevID = ""

	n = numpy.zeros((len(rows), dims))
	for i, row in enumerate(rows):
		n[i] = values[row]
	return n


############## Value classification ##############


# allValuesArray: contains all values from which a classification is computed
# valueArray: contains the values for which the class is determined
def medmw(valueArray, allValuesArray, nbSegments):
	bins = []
	mwSim = numpy.mean(allValuesArray)
	lowerValues = sorted([x for x in allValuesArray if x < mwSim])
	for i in range(1, (nbSegments // 2) + 1):
		lowerPos = (i-1) * len(lowerValues) // (nbSegments // 2)
		bins.append(lowerValues[lowerPos])
	bins.append(mwSim)
	upperValues = sorted([x for x in allValuesArray if x >= mwSim])
	for i in range(1, (nbSegments // 2) + 1):
		upperPos = i * len(upperValues) // (nbSegments // 2) - 1
		bins.append(upperValues[upperPos])
	classArray = numpy.digitize(valueArray, bins[:-1])
	return classArray


# renamed to minmw (field length limitations in arcgis)
# allValuesArray: contains all values from which a classification is computed
# valueArray: contains the values for which the class is determined
def minmw(valueArray, allValuesArray, nbSegments):
	(histogram, lowerBinEdges) = numpy.histogram(allValuesArray, bins=nbSegments // 2, range=(valueArray.min(), valueArray.mean()))
	(histogram, upperBinEdges) = numpy.histogram(allValuesArray, bins=nbSegments // 2, range=(valueArray.mean(), valueArray.max()))
	binEdges = numpy.concatenate((lowerBinEdges[:-1], upperBinEdges[:-1]))
	classArray = numpy.digitize(valueArray, binEdges)
	return classArray


def eqint(valueArray, allValuesArray, nbSegments):
	bins = numpy.linspace(numpy.amin(allValuesArray), numpy.amax(allValuesArray), num=nbSegments, endpoint=False)
	classArray = numpy.digitize(valueArray, bins)
	return classArray


def classify(valueArray, classificationTuples, allValueArray=None):
	classMatrix = valueArray.copy()
	classHeaders = ["VALUE"]
	for ct in classificationTuples:
		if len(ct) == 2:
			(algo, nbClasses) = ct
			print("Classify using", algo, "with", nbClasses, "classes")
			classArray = globals()[algo](valueArray, valueArray, nbClasses)
			classMatrix = numpy.vstack((classMatrix, classArray))
			classHeaders.append("{}{}".format(algo.upper(), nbClasses))
		elif (len(ct) == 3) and (ct[2] == "US"):
			(algo, nbClasses, suffix) = ct
			print("Classify using", algo, "with", nbClasses, "classes (unique scale)")
			classArray = globals()[algo](valueArray, allValueArray, nbClasses)
			classMatrix = numpy.vstack((classMatrix, classArray))
			classHeaders.append("{}{}{}".format(algo.upper(), nbClasses, suffix))
	return (classMatrix.transpose(), classHeaders)


############## Experiments ##############


def simExperiment(dataMatrixNames, similarityMeasures, geoMatrixName="", percentData=False):
	if geoMatrixName != "":
		geoMatrix, geoRows = loadSimilarityMatrix(geoMatrixName)
		geoMatrix = invertMatrix(geoMatrix)

	for simMatrixPrefix, dataMatrixName in dataMatrixNames.items():
		if percentData:
			(dataMatrix, _, rows) = loadPercentDataMatrix(dataMatrixName)
		else:
			(dataMatrix, _, rows) = loadDataMatrix(dataMatrixName)

		for simMeasure in similarityMeasures:
			simMatrix = computeSimilarityMatrix(dataMatrix, rows, simMeasure)
			writeMatrix(simMatrix, "{}-{}-sim.csv".format(simMatrixPrefix, simMeasure), rows, rows)
			if geoMatrixName != "":
				fGeoMatrix, _ = filterSimilarityMatrix(geoMatrix, geoRows, rows)
				print("Linc:", linc(simMatrix, fGeoMatrix, rows))


def paramExperiment(simMatrixNames, parameters, classificationTuples):
	rowTitles = {}			# id => rows
	paramMatrices = {}		# id,param => paramMatrix
	allParamMatrices = {}	# param => paramMatrix [concatenate over different ids]

	for simMatrixName in simMatrixNames:
		simMatrix, rows = loadSimilarityMatrix(simMatrixName)
		id = simMatrixName.replace("-sim.csv", "")
		rowTitles[id] = rows
		for param in parameters:
			pmid = (id, param)
			paramMatrices[pmid] = computeParameterMatrix(simMatrix, param)
			if param in allParamMatrices:
				allParamMatrices[param] = numpy.concatenate((allParamMatrices[param], paramMatrices[pmid]))
			else:
				allParamMatrices[param] = paramMatrices[pmid].copy()

	for (id, param) in paramMatrices:
		(finalMatrix, headers) = classify(paramMatrices[(id, param)], classificationTuples, allParamMatrices[param])
		writeMatrix(finalMatrix, "{}-{}.csv".format(id, param), rowTitles[id], headers)


def correlExperiment(correlationTuples, classificationTuples):
	rowTitles = {}
	paramMatrices = {}
	allParamMatrices = None

	for (id, sim1, sim2) in correlationTuples:
		simMatrix1, rows1 = loadSimilarityMatrix(sim1)
		simMatrix2, rows2 = loadSimilarityMatrix(sim2)
		if rows1 != rows2:
			print("Rows don't match, taking intersection")
			simMatrix1, rows1 = filterSimilarityMatrix(simMatrix1, rows1, rows2)
			simMatrix2, rows2 = filterSimilarityMatrix(simMatrix2, rows2, rows1)
		rowTitles[id] = rows1
		paramMatrices[id] = computeCorrelationMatrix(simMatrix1, simMatrix2)
		if allParamMatrices != None:
			allParamMatrices = numpy.concatenate((allParamMatrices, paramMatrices[id]))
		else:
			allParamMatrices = paramMatrices[id].copy()

	for id in paramMatrices:
		(finalMatrix, headers) = classify(paramMatrices[id], classificationTuples, allParamMatrices)
		writeMatrix(finalMatrix, "{}.csv".format(id), rowTitles[id], headers)


def geoCorrelExperiment(simMatrixNames, geoMatrixName, classificationTuples):
	paramMatrices = {}
	allParamMatrices = None
	(geoSimMatrix, geoColumns) = loadSimilarityMatrix(geoMatrixName)
	geoSimMatrix = invertMatrix(geoSimMatrix)

	for simMatrixName in simMatrixNames:
		simMatrix, dataRows = loadSimilarityMatrix(simMatrixName)
		id = simMatrixName.replace("-sim.csv", "")
		if dataRows != geoColumns:
			print("Rows don't match, reducing geoMatrix")
			fgeoSimMatrix, fGeoColumns = filterSimilarityMatrix(geoSimMatrix, geoColumns, dataRows)
			paramMatrices[id] = computeCorrelationMatrix(simMatrix, fGeoSimMatrix)
		else:
			paramMatrices[id] = computeCorrelationMatrix(simMatrix, geoSimMatrix)
		if allParamMatrices != None:
			allParamMatrices = numpy.concatenate((allParamMatrices, paramMatrices[id]))
		else:
			allParamMatrices = paramMatrices[id].copy()

	for id in paramMatrices:
		(finalMatrix, headers) = classify(paramMatrices[id], classificationTuples, allParamMatrices)
		writeMatrix(finalMatrix, "{}-{}.csv".format(id), geoColumns, headers)


def clusterExperiment(simMatrixNames, clusterTuples):
	for simMatrixName in simMatrixNames:
		simm, rows = loadSimilarityMatrix(simMatrixName)
		clusterMatrix = None
		clusterColumns = []
		for algo, nclust in clusterTuples:
			clum = cluster(simm, rows, algo, nclust)
			if clusterMatrix != None:
				clusterMatrix = numpy.hstack((clusterMatrix, clum))
			else:
				clusterMatrix = clum
			print(clum.shape, clusterMatrix.shape)
			clusterColumns.append("{}{}".format(algo.upper(), nclust))
			# todo: output dendrogram
		writeMatrix(clusterMatrix, simMatrixName.replace("-sim.csv", "-clu.csv"), rows, clusterColumns)


def mdsExperiment(simMatrixNames, ndim):
	for simMatrixName in simMatrixNames:
		simm, rows = loadSimilarityMatrix(simMatrixName)
		mdsMatrix = mds(simm, rows, ndim)
		writeMatrix(mdsMatrix, simMatrixName.replace("-sim.csv", "-mds{}.csv".format(ndim)), rows, ["MDS{}".format(x) for x in range(1, ndim+1)])
