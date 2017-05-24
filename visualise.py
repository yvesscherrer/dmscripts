#!  python
# -*- coding: iso-8859-1 -*-

import arcpy, os

arcpy.env.qualifiedFieldNames = False


def createShpFile(datafile, shpmodelfile, outshp):
	print "Create shp:", datafile, "=>", outshp
	arcpy.MakeFeatureLayer_management(shpmodelfile, "temp_layer")
	arcpy.AddJoin_management("temp_layer", "BFS", datafile, "LOC", join_type="KEEP_COMMON")
	arcpy.CopyFeatures_management("temp_layer", outshp)
	arcpy.DeleteField_management(outshp, ["ORIG_FID", "LOC_X", "LOC_Y"])
	arcpy.Delete_management("temp_layer")
	print "Done"


def createVisualisation(shpfile, mxdfile, lyrfile, manualBreakValues, outlyr="", outpdf="", outpng=""):
	print "Create png/pdf:", shpfile, "=>", outlyr, outpdf, outpng
	mxd = arcpy.mapping.MapDocument(mxdfile)
	df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
	shp = arcpy.mapping.Layer(shpfile)
	lyr = arcpy.mapping.Layer(lyrfile)
	arcpy.mapping.UpdateLayer(df, shp, lyr, True)

	print shp.symbologyType
	if manualBreakValues != []:
		shp.symbology.classBreakValues = manualBreakValues
	elif shp.symbologyType == "GRADUATED_COLORS":
		shp.symbology.reclassify()

	if outlyr != "":
		shp.saveACopy(outlyr)
	arcpy.mapping.AddLayer(df, shp)
	if outpdf != "":
		arcpy.mapping.ExportToPDF(mxd, outpdf)
	if outpng != "":
		arcpy.mapping.ExportToPNG(mxd, outpng, resolution=300)
	del shp, df, mxd, lyr
	print "Done"

##############################################

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
	createShpFile(csvpath + filename, shpmodel, shppath + shpname)
	pngname = shpname.replace(".shp", ".png")
	if "-clu" in filename:		# categorical features
		lyrfile = basepath + "rawshp/point_clu6.lyr"
		createVisualisation(shppath + shpname, mxdfile, lyrfile, [], "", "", pngpath + pngname)
	else:
		lyrfile = basepath + "rawshp/point_value_6jenks.lyr"
		createVisualisation(shppath + shpname, mxdfile, lyrfile, [], "", "", pngpath + pngname)
