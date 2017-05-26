#! /usr/bin/python3
# -*- coding: utf-8 -*-

import vdmclone

vdmclone.inputencoding = 'iso-8859-1'
vdmclone.inputdelimiter = ';'
vdmclone.outputencoding = 'iso-8859-1'
vdmclone.outputdelimiter = ';'
vdmclone.variablevariantdelim = "."

def experiment(ids, outid, algo="wm"):
	first = True
	for id in ids:
		print(id)
		(dataMatrix, columns, rows) = vdmclone.loadPercentDataMatrix("../2_datatables/{}.csv".format(id))
		if first:
			fullDataMatrix, fullColumns, fullRows = dataMatrix, columns, rows
			first = False
		else:
			fullDataMatrix, fullColumns, fullRows = vdmclone.mergeDataMatrices(fullDataMatrix, fullColumns, fullRows, dataMatrix, columns, rows)
	simMatrix = vdmclone.computeSimilarityMatrix(fullDataMatrix, fullRows, "EuclidRIW")
	vdmclone.writeMatrix(simMatrix, "{}-sim.csv".format(outid), fullRows, fullRows)
	vdmclone.clusterExperiment(["{}-sim.csv".format(outid)], [(algo, i) for i in range(2, 21)])


def shibbolethExperiment(algo="wm"):
	(dataMatrix, columns, rows) = vdmclone.loadPercentDataMatrix2("../2_shibboleth/lexEuro12_singledept.csv")
	print(columns, rows)
	simMatrix = vdmclone.computeSimilarityMatrix(dataMatrix, rows, "EuclidRIW2")
	vdmclone.writeMatrix(simMatrix, "neighbors-{}-sim.csv".format(algo), rows, rows)
	vdmclone.clusterExperiment(["neighbors-{}-sim.csv".format(algo)], [(algo, i) for i in range(2, 21)])


def filterExperiment(filterfile, filtercolumn, algo="wm", nbClusters=range(2, 21)):
	m1, c1, r1 = vdmclone.loadFilteredPercentDataMatrix("../2_datatables/lexEuro1_dept_aggrp.csv", filterfile, filtercolumn, filterenc="utf-8-sig")
	m2, c2, r2 = vdmclone.loadFilteredPercentDataMatrix("../2_datatables/lexEuro2_dept_aggrp.csv", filterfile, filtercolumn, filterenc="utf-8-sig")
	m3, c3, r3 = vdmclone.mergeDataMatrices(m1, c1, r1, m2, c2, r2)
	print(len(m3), len(c3), len(r3))
	simMatrix = vdmclone.computeSimilarityMatrix(m3, r3, "EuclidRIW")
	vdmclone.writeMatrix(simMatrix, "{}-{}-sim.csv".format(filtercolumn, algo), r3, r3)
	vdmclone.clusterExperiment(["{}-{}-sim.csv".format(filtercolumn, algo)], [(algo, i) for i in nbClusters])


if __name__ == "__main__":
	experiment(["lexEuro1_dept_aggrp"], "lexEuro1_dept")
	experiment(["lexEuro1_dist_aggrp"], "lexEuro1_dist")
	experiment(["lexEuro2_dept_aggrp"], "lexEuro2_dept")
	experiment(["lexEuro2_dist_aggrp"], "lexEuro2_dist")
	experiment(["lexEuro1_dept_aggrp", "lexEuro2_dept_aggrp"], "lexEuro12_dept")
	experiment(["lexEuro1_dist_aggrp", "lexEuro2_dist_aggrp"], "lexEuro12_dist")
	experiment(["lexEuro1_dept_aggrp", "lexEuro2_dept_aggrp"], "lexEuro12_dept_wa", algo="wa")
	shibbolethExperiment(algo="wm")
	shibbolethExperiment(algo="wa")
	filterExperiment("../2_featselect_skl/univariate_chi2_topn.variants.csv", "TOP150")
	filterExperiment("../2_featselect_skl/svm-rfe.variants.csv", "SVM_RFE_TOP15", nbClusters=range(2, 16))
	filterExperiment("../2_featselect_skl/svm-rfe.variants.csv", "SVM_RFE_TOP20", nbClusters=range(2, 16))
	filterExperiment("../2_featselect_skl/svm-rfe.variants.csv", "SVM_RFE_TOP25", nbClusters=range(2, 16))
	filterExperiment("../2_featselect_skl/svm-rfe.variants.csv", "SVM_RFE_TOP30", nbClusters=range(2, 16))
	filterExperiment("../2_featselect_skl/maxent-rfe.variants.csv", "ME_RFE_TOP15", nbClusters=range(2, 16))
	filterExperiment("../2_featselect_skl/maxent-rfe.variants.csv", "ME_RFE_TOP20", nbClusters=range(2, 16))
	filterExperiment("../2_featselect_skl/maxent-rfe.variants.csv", "ME_RFE_TOP25", nbClusters=range(2, 16))
	filterExperiment("../2_featselect_skl/maxent-rfe.variants.csv", "ME_RFE_TOP30", nbClusters=range(2, 16))
