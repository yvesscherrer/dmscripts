#!  python
# -*- coding: iso-8859-1 -*-

# this requires ArcGIS and can only be executed from Windows Python (the one installed with ArcGIS)
import arcinterface, os


basepath = "C:/Users/yvessche/switchdrive/dialectometry-stuff/vdmclone-sds-sads/"
csvpath = basepath + "csv/"
#shpmodel = basepath + "rawshp/377polygons_C.shp" # no lakes
shpmodel = basepath + "rawshp/377polygons_CL.shp" # with lakes
mxdpath = basepath + "rawshp/"
mxdfile = mxdpath + "document.mxd"
shppath = basepath + "shp/"
lyrpath = basepath + "lyr/"
pdfpath = basepath + "pdf/"
pngpath = basepath + "png/"

if "shp" not in os.listdir(basepath):
	os.mkdir(shppath)
#if "pdf" not in os.listdir(basepath):
#	os.mkdir(pdfpath)
if "png" not in os.listdir(basepath):
	os.mkdir(pngpath)

for filename in os.listdir(csvpath):
	if "-sim" in filename:
		continue
	shpname = filename.replace("-", "_").replace(".csv", ".shp")
	arcinterface.joinCsvWithShp(csvpath + filename, shpmodel, shppath + shpname, "LOC", "BFS", ["ORIG_FID", "LOC_X", "LOC_Y"])

	fileid = filename.replace(".csv", "")
	for field in ("MEDMW20", "EQINT20", "MEDMW20US", "EQINT20US"):
		arcinterface.createVisualisation(shppath + shpname, mxdfile, mxdpath + field + ".lyr", [], lyrpath + fileid + "_" + field + ".lyr", "", pngpath + fileid + "-" + field + ".png")


# old stuff...
#for filename in os.listdir(shppath):
#	if not filename.endswith(".shp"):
#		continue
#	fileid = filename.replace(".shp", "")
#	createVisualisation(shppath + filename, mxdfile, mxdpath + "MEDMW6.lyr", [], lyrpath + fileid + "_MEDMW6.lyr", "", pngpath + fileid + "_MEDMW6.png")
#	createVisualisation(shppath + filename, mxdfile, mxdpath + "VALUE20.lyr", [], lyrpath + fileid + "_VALUE20.lyr", "", pngpath + fileid + "_VALUE20.png")
#	if ("correl" in fileid) or ("min" in fileid) or ("max" in fileid) or ("mean" in fileid):
#		breakValues = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0] 		# works for parameters between 0 and 1, i.e. max, min, mean, correl(?)
#		createVisualisation(shppath + filename, mxdfile, mxdpath + "VALUE20.lyr", breakValues, lyrpath + fileid + "_VALUE20UniqScale.lyr", "", pngpath + fileid + "_VALUE20UniqScale.png")
