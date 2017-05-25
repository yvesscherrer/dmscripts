#! /usr/bin/python3
# -*- coding: utf-8 -*-

import vdmclone, os

vdmclone.inputencoding = 'iso-8859-1'
vdmclone.inputdelimiter = ';'
vdmclone.outputencoding = 'iso-8859-1'
vdmclone.outputdelimiter = ';'

def sads():
	vdmclone.simExperiment({"csv/sads-68{}".format(ftype): "data/sads-68{}.csv".format(ftype) for ftype in ("ex", "over30", "over40", "over50", "dom")}, ["JaccardRIW"])
	vdmclone.paramExperiment(["csv/sads-68{}-JaccardRIW-sim.csv".format(ftype) for ftype in ("ex", "over30", "over40", "over50", "dom")], ["max", "min", "mean", "stddev", "skew"], [("minmw", 6), ("medmw", 6)])


def sds():
	vdmclone.simExperiment({"csv/sds-{}".format(level): "data/sds-{}.csv".format(level) for level in ("all", "phon", "morph", "lex")}, ["JaccardRIW"])
	vdmclone.paramExperiment(["csv/sds-{}-JaccardRIW-sim.csv".format(level) for level in ("all", "phon", "morph", "lex")], ["max", "min", "mean", "stddev", "skew"], [("minmw", 6), ("medmw", 6)])

def correl():
	vdmclone.simExperiment({"csv/phon": "data/sds-phon.csv", "csv/morph": "data/sds-morph.csv", "csv/lex": "data/sds-lex.csv", "csv/synt": "data/sads-68dom.csv", "csv/all": "data/sds-all.csv"}, ["JaccardRIW"])
	comparisons = [("csv/correl-{}-{}".format(x[0], x[1]), "csv/{}-JaccardRIW-sim.csv".format(x[0]), "csv/{}-JaccardRIW-sim.csv".format(x[1])) for x in [("phon", "morph"), ("phon", "lex"), ("phon", "synt"), ("morph", "lex"), ("morph", "synt"), ("lex", "synt")]]
	vdmclone.correlExperiment(comparisons, [("minmw", 6), ("medmw", 6)])
	files = ["csv/{}-JaccardRIW-sim.csv".format(x) for x in ("phon", "morph", "lex", "synt", "all")]
	vdmclone.geoCorrelExperiment(files, "data/geodist.csv", [("minmw", 6), ("medmw", 6)])


def sims():
	dataids = ("sds-all", "sds-phon", "sds-morph", "sds-lex", "sads-68ex", "sads-68dom", "sads-68over30", "sads-68over40", "sads-68over50", "sads68dom-sdsall")
	vdmclone.simExperiment({"csv/{}".format(x.replace("-", "").replace("sads68domsdsall", "all")): "data/{}.csv".format(x) for x in dataids}, ["JaccardRIW"])

# all below require sims()

def parameters():
	dataids = ("sdsall", "sdsphon", "sdsmorph", "sdslex", "sads68ex", "sads68dom", "sads68over30", "sads68over40", "sads68over50", "all")
	parameters = ("max", "min", "mean", "stddev", "skew")
	classes = (("minmw", 20), ("medmw", 20), ("eqint", 20), ("minmw", 20, "US"), ("medmw", 20, "US"), ("eqint", 20, "US"))
	vdmclone.paramExperiment(["csv/{}-JaccardRIW-sim.csv".format(x) for x in dataids], parameters, classes)


def levelcorrelations():
	comparisons = [("csv/correl-{}-{}".format(x[0], x[1]), "csv/{}-JaccardRIW-sim.csv".format(x[0]), "csv/{}-JaccardRIW-sim.csv".format(x[1])) for x in [("sdsphon", "sdsmorph"), ("sdsphon", "sdslex"), ("sdsphon", "sads68dom"), ("sdsmorph", "sdslex"), ("sdsmorph", "sads68dom"), ("sdslex", "sads68dom"), ("sads68ex", "sads68dom")]]
	classes = (("minmw", 20), ("medmw", 20), ("eqint", 20), ("minmw", 20, "US"), ("medmw", 20, "US"), ("eqint", 20, "US"))
	vdmclone.correlExperiment(comparisons, classes)


def levelcorrelations2():
	comparisons = [("csv/correl-{}-{}".format(x[0], x[1]), "csv/{}-JaccardRIW-sim.csv".format(x[0]), "csv/{}-JaccardRIW-sim.csv".format(x[1])) for x in [("all", "sdsphon"), ("all", "sdsmorph"), ("all", "sdslex"), ("all", "sads68dom")]]
	classes = (("minmw", 20), ("medmw", 20), ("eqint", 20), ("minmw", 20, "US"), ("medmw", 20, "US"), ("eqint", 20, "US"))
	vdmclone.correlExperiment(comparisons, classes)


def geocorrelations():
	dataids = ["csv/{}-JaccardRIW-sim.csv".format(x) for x in ("sdsall", "sdsphon", "sdsmorph", "sdslex", "sads68ex", "sads68dom", "all")]
	geofile = "data/geodist.csv"
	classes = (("minmw", 20), ("medmw", 20), ("eqint", 20), ("minmw", 20, "US"), ("medmw", 20, "US"), ("eqint", 20, "US"))
	vdmclone.geoCorrelExperiment(dataids, geofile, classes)

if __name__ == "__main__":
	if "csv" not in os.listdir("."):
		os.mkdir("csv")
	#sads()
	#sds()
	#correl()
	sims()
	parameters()
	levelcorrelations()
	levelcorrelations2()
	geocorrelations()
