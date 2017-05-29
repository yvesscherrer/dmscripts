#! /usr/bin/python3
# -*- coding: utf-8 -*-

import csv, vdmclone, math, numpy

# 2 data matrices => 1 data matrix with difference values
def Euclid(a, b):
	variablesum = 0.0
	nbcomp = 0
	for key in set(a.keys()) | set(b.keys()):
		variablesum += (a.get(key, 0.0) - b.get(key, 0.0)) ** 2
		nbcomp += 1
	return math.sqrt(variablesum/nbcomp)


def createDiffDataMatrix(infilename1, infilename2, outfilename):
	m1, c1, r1 = vdmclone.loadPercentDataMatrix(infilename1)
	m2, c2, r2 = vdmclone.loadPercentDataMatrix(infilename2)
	m3, r3 = [], []
	if c1 != c2:
		print("column mismatch")
		return
	for loc in r1:
		if loc in r2:
			i1 = r1.index(loc)
			i2 = r2.index(loc)
			distRow = [Euclid(m1[i1][c], m2[i2][c]) for c in range(len(c1))]
			m3.append(distRow)
			r3.append(loc)
	vdmclone.writeMatrix(numpy.array(m3), outfilename, r3, c1)


# 2 data matrices => 1 parameter matrix with the parameter "mean Euclidean difference"
def createDiffParam(infilename1, infilename2, outfilename):
	m1, c1, r1 = vdmclone.loadPercentDataMatrix(infilename1)
	m2, c2, r2 = vdmclone.loadPercentDataMatrix(infilename2)
	if c1 != c2:
		print("column mismatch")
		return
	m3, r3 = [], []
	for loc in r1:
		if loc in r2:
			diffsum = 0
			for var1, var2 in zip(m1[r1.index(loc)], m2[r2.index(loc)]):
				diff = math.sqrt(sum([(var1.get(x, 0)-var2.get(x, 0))**2 for x in var1.keys() | var2.keys()]))
				diffsum += diff
			m3.append(diffsum / len(c1))
			r3.append(loc)
	vdmclone.writeMatrix(numpy.array(m3), outfilename, r3, ["VALUE"])


# 2 parameter matrices => 1 parameter matrix with the diff of the two
def computeParamDiff(matrixname1, matrixname2, outname, absolute=False):
	matrix1 = vdmclone.loadParamMatrix(matrixname1)
	matrix2 = vdmclone.loadParamMatrix(matrixname2)
	diffmatrix = []
	rowHeaders = []
	for k in sorted(matrix1):
		if k in matrix2:
			rowHeaders.append(k)
			if absolute:
				diffmatrix.append(abs(matrix1[k] - matrix2[k]))
			else:
				diffmatrix.append(matrix1[k] - matrix2[k])
	vdmclone.writeMatrix(numpy.array(diffmatrix), outname, rowHeaders, ["VALUE"])


def loadPercentDiffMatrix(infilename):
	print("Loading percent diff matrix from file", infilename)
	columnheaders = []
	rowheaders = []
	data = []
	rd = csv.reader(open(infilename, 'r', encoding="utf-8-sig"), delimiter=",")
	first = True
	for line in rd:
		if first:
			columnheaders = line[1:]
			first = False
		else:
			rowheaders.append(line[0])
			data.append([float(x) for x in line[1:]])
	numpydata = numpy.array(data)
	return (numpydata, columnheaders, rowheaders)


def averageByPlace(infilename, outfilename):
	m, c, r = loadPercentDiffMatrix(infilename)
	mean = numpy.mean(m, axis=1)
	std = numpy.std(m, axis=1)
	meanstd = numpy.vstack((mean.T, std.T)).T
	vdmclone.writeMatrix(meanstd, outfilename, r, ["MEAN", "STDDEV"])


def averageByVariable(infilename, outfilename):
	m, c, r = loadPercentDiffMatrix(infilename)
	mean = numpy.mean(m, axis=0)
	std = numpy.std(m, axis=0)
	meanstd = numpy.vstack((mean.T, std.T)).T
	vdmclone.writeMatrix(meanstd, outfilename, c, ["MEAN", "STDDEV"])

# if __name__ == "__main__":
# 	averageByPlace("data/diff-3j3a.csv", "data/diff-3j3a-byplace.csv")
# 	averageByVariable("data/diff-3j3a.csv", "data/diff-3j3a-byvar.csv")
