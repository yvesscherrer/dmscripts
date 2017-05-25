#!  python
# -*- coding: iso-8859-1 -*-

# this requires ArcGIS and can only be executed from Windows Python (the one installed with ArcGIS)
import arcinterface, os

basepath = "C:/Users/yvessche/switchdrive/dialectometry-stuff/sads-malaga/"
csvpath = basepath + "csv/"
shpmodel = basepath + "rawshp/sads_points.shp"
mxdfile = basepath + "rawshp/sads.mxd"
shppath = basepath + "shp/"
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
	if "-mds" in filename:	# mds not supported yet
		continue
	shpname = filename.replace("-", "_").replace(".csv", ".shp")
	arcinterface.joinCsvWithShp(csvpath + filename, shpmodel, shppath + shpname, "LOC", "BFS", ["ORIG_FID", "LOC_X", "LOC_Y"])
	pngname = shpname.replace(".shp", ".png")
	if "-clu" in filename:		# categorical features
		lyrfile = basepath + "rawshp/point_clu6.lyr"
		arcinterface.createVisualisation(shppath + shpname, mxdfile, lyrfile, [], "", "", pngpath + pngname)
	else:
		lyrfile = basepath + "rawshp/point_value_6jenks.lyr"
		arcinterface.createVisualisation(shppath + shpname, mxdfile, lyrfile, [], "", "", pngpath + pngname)
