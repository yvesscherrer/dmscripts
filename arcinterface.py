#!  python
# -*- coding: iso-8859-1 -*-

# this requires ArcGIS and can only be executed from Windows Python (the one installed with ArcGIS)
import arcpy

arcpy.env.qualifiedFieldNames = False


def joinCsvWithShp(csvfile, shpmodelfile, outshpfile, csvfield, shpfield, removeFields=[]):
	print "Create shp:", csvfile, "=>", outshpfile
	arcpy.MakeFeatureLayer_management(shpmodelfile, "temp_layer")
	arcpy.AddJoin_management("temp_layer", shpfield, csvfile, csvfield, join_type="KEEP_COMMON")
	arcpy.CopyFeatures_management("temp_layer", outshpfile)
	if removeFields != []:
		arcpy.DeleteField_management(outshpfile, removeFields)
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
