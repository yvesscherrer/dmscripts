#! /usr/bin/python3
# -*- coding: utf-8 -*-

import vdmclone, os, difftools


if "csv" not in os.listdir("."):
	os.mkdir("csv")

for x in (("2j", "2a"), ("3j", "3m"), ("3j", "3a"), ("3m", "3a")):
	difftools.createDiffDataMatrix("data/{}.csv".format(x[0]), "data/{}.csv".format(x[1]), "data/diff{}{}.csv".format(x[0], x[1]))
	difftools.createDiffParam("data/{}.csv".format(x[0]), "data/{}.csv".format(x[1]), "csv/{}{}-EuclidDiff.csv".format(x[0], x[1]))

vdmclone.simExperiment({"csv/{}".format(x): "data/{}.csv".format(x) for x in ("2j", "2a", "3j", "3m", "3a")}, ["EuclidRIW", "Euclid"], geoMatrixName="origdata/geodist.csv", percentData=True)
vdmclone.simExperiment({"csv/{}".format(x): "data/{}.csv".format(x) for x in ("diff3j3m", "diff3j3a", "diff3m3a")}, ["EuclidRIW2"], geoMatrixName="origdata/geodist.csv", percentData=True, splitVariables=False)

vdmclone.paramExperiment(["csv/{}-Euclid-sim.csv".format(x) for x in ("2j", "2a", "3j", "3m", "3a")], ["mean", "stddev", "skew"], [("minmw", 6), ("medmw", 6)])
vdmclone.paramExperiment(["csv/{}-EuclidRIW2-sim.csv".format(x) for x in ("diff3j3m", "diff3j3a", "diff3m3a")], ["mean", "stddev", "skew"], [("minmw", 6), ("medmw", 6)])

for param in ("mean", "stddev", "skew"):
	for x in (("2j", "2a"), ("3j", "3m"), ("3j", "3a"), ("3m", "3a")):
		difftools.computeParamDiff("csv/{}-Euclid-{}.csv".format(x[0], param), "csv/{}-Euclid-{}.csv".format(x[1], param), "csv/{}{}-Euclid-{}diff.csv".format(x[0], x[1], param))

vdmclone.correlExperiment([("csv/3j3a-Euclid-correl", "csv/3j-Euclid-sim.csv", "csv/3a-Euclid-sim.csv"), ("csv/3j3m-Euclid-correl", "csv/3j-Euclid-sim.csv", "csv/3m-Euclid-sim.csv"), ("csv/3m3a-Euclid-correl", "csv/3m-Euclid-sim.csv", "csv/3a-Euclid-sim.csv")], [("minmw", 6, "US"), ("medmw", 6, "US")])

vdmclone.clusterExperiment(["csv/{}-Euclid-sim.csv".format(x) for x in ("2j", "2a", "3j", "3m", "3a")], [("wm", 6)])

vdmclone.mdsExperiment(["csv/{}-Euclid-sim.csv".format(x) for x in ("2j", "2a", "3j", "3m", "3a")], 3)
