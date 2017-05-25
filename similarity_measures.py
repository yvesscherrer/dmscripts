#! /usr/bin/python3
# -*- coding: utf-8 -*-

import vdmclone

vdmclone.inputencoding = 'iso-8859-1'
vdmclone.inputdelimiter = ';'
vdmclone.outputencoding = 'iso-8859-1'
vdmclone.outputdelimiter = ';'

datamatrices = ("sds-phon.csv", "sds-morph.csv", "sds-lex.csv", "sads-68dom.csv", "sads68dom-sdsall.csv")
metrics = ("RIW", "RandomRIW", "RandomRIW", "JaccardRIW", "DiceRIW", "OverlapRIW", "Hamming")
outfile = open("similarity_measures.txt", "w")

outfile.write("Dataset\tMultiple")
for m in metrics:
	outfile.write("\t" + m)
outfile.write("\n")

geoMatrix, geoColumns = vdmclone.loadSimilarityMatrix("data/geodist.csv")

for d in datamatrices:
	dataMatrix, dataColumns, dataRows = vdmclone.loadDataMatrix("data/" + d)
	multi = vdmclone.countMultipleAnswers(dataMatrix)
	outfile.write("{}\t{:.4f}%".format(d, 100*multi))
	for m in metrics:
		simMatrix = vdmclone.computeSimilarityMatrix(dataMatrix, dataRows, m)
		if dataRows != geoColumns:
			print("Columns don't match!")
			print(dataRows)
			print(geoColumns)
		else:
			lincVal = vdmclone.linc(simMatrix, geoMatrix, dataRows)
			print(lincVal)
			outfile.write("\t{:.4f}".format(lincVal))
	outfile.write("\n")
print("done")
