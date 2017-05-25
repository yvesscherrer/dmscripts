#! /usr/bin/python3
# -*- coding: utf-8 -*-

import vdmclone

vdmclone.inputencoding = 'iso-8859-1'
vdmclone.inputdelimiter = ';'
vdmclone.outputencoding = 'iso-8859-1'
vdmclone.outputdelimiter = ';'


simm, headers = vdmclone.loadSimilarityMatrix("results34.ppl.4gr.csv")
simm = vdmclone.invertMatrix(simm)	# ppl matrices are in fact distance matrices
headers = [x.replace("ID", "") for x in headers]
clum = vdmclone.cluster(simm, headers, "wm", 6)
vdmclone.writeMatrix(clum, "results34.ppl.4gr.6wm.csv", rowHeaders=headers, columnHeaders=["CLU"])

simm, headers = vdmclone.loadSimilarityMatrix("results34.kld.4gr.csv")
simm = vdmclone.invertMatrix(simm)	# kld matrices are in fact distance matrices
headers = [x.replace("ID", "") for x in headers]
clum = vdmclone.cluster(simm, headers, "wa", 6)
vdmclone.writeMatrix(clum, "results34.kld.4gr.6wa.csv", rowHeaders=headers, columnHeaders=["CLU"])

simm, headers = vdmclone.loadSimilarityMatrix("results34.ppl.4gr.csv")
simm = vdmclone.invertMatrix(simm)	# ppl matrices are in fact distance matrices
headers = [x.replace("ID", "") for x in headers]
for (algo, nclust) in (("wm", 6), ("wm", 10), ("wa", 6), ("wm", 10)):
	clum = vdmclone.cluster(simm, headers, algo, nclust)
	vdmclone.writeMatrix(clum, "results34.ppl.4gr.{}{}.csv".format(nclust, algo), rowHeaders=headers, columnHeaders=["CLU"])

simm, headers = vdmclone.loadSimilarityMatrix("results34.ppl.4gr.csv")
simm = vdmclone.invertMatrix(simm)	# ppl matrices are in fact distance matrices
headers = [x.replace("ID", "") for x in headers]
for i in (1, 3):
	mdsm = vdmclone.mds(simm, headers, i)
	vdmclone.writeMatrix(mdsm, "results34.ppl.4gr.mds{}.csv".format(i), rowHeaders=headers, columnHeaders=["MDS{}".format(x) for x in range(1, i+1)])
