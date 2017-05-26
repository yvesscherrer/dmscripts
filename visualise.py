#!  python
# -*- coding: iso-8859-1 -*-

import arcpy, os, arcinterface

arcpy.env.qualifiedFieldNames = False


def createVisualisations(mxdfile, shpfile, lyrfile, fieldprefix, outdir):
	print "Export images from", shpfile
	mxd = arcpy.mapping.MapDocument(mxdfile)
	df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
	shp = arcpy.mapping.Layer(shpfile)
	lyr = arcpy.mapping.Layer(lyrfile)
	arcpy.mapping.UpdateLayer(df, shp, lyr, True)

	fieldnames = [field.name for field in arcpy.ListFields(shpfile, fieldprefix+"*")]
	for fieldname in fieldnames:
		print fieldname
		shp.symbology.valueField = fieldname
		shp.symbology.addAllValues()
		arcpy.mapping.AddLayer(df, shp)
		arcpy.mapping.ExportToPNG(mxd, outdir + "/" + fieldname + ".png", resolution=300)
		arcpy.mapping.RemoveLayer(df, shp)


def experiment(id, localizer):
	basepath = "C:/Users/yvessche/switchdrive/avanzi/3_dm_clustering"
	csvpath = basepath + "/{}-clu.csv".format(id)
	shpmodel = "C:/Users/yvessche/switchdrive/avanzi/geodata/{}_poly.shp".format(localizer)
	shppath = basepath + "/" + id
	if id not in os.listdir(basepath):
		os.mkdir(shppath)
	arcinterface.joinCsvWithShp(csvpath, shpmodel, shppath + "/data.shp", "LOC", "LOC", removeFields=["LOC_1"])
	if "wa" in id:
		createVisualisations(basepath + "/cluster.mxd", shppath + "/data.shp", basepath + "/cluster.lyr", "WA", shppath)
	else:
		createVisualisations(basepath + "/cluster.mxd", shppath + "/data.shp", basepath + "/cluster.lyr", "WM", shppath)


if __name__ == "__main__":
	experiment("lexEuro1_dept", "departements")
	experiment("lexEuro1_dist", "districts")
	experiment("lexEuro2_dept", "departements")
	experiment("lexEuro2_dist", "districts")
	experiment("lexEuro12_dept", "departements")
	experiment("lexEuro12_dist", "districts")
	experiment("lexEuro12_dept_wa", "departements")
	experiment("neighbors-wa", "departements")
	experiment("neighbors-wm", "departements")

	experiment("TOP150-wm", "departements")
	experiment("SVM_RFE_TOP15-wm", "departements")
	experiment("SVM_RFE_TOP20-wm", "departements")
	experiment("SVM_RFE_TOP25-wm", "departements")
	experiment("SVM_RFE_TOP30-wm", "departements")
	experiment("ME_RFE_TOP15-wm", "departements")
	experiment("ME_RFE_TOP20-wm", "departements")
	experiment("ME_RFE_TOP25-wm", "departements")
	experiment("ME_RFE_TOP30-wm", "departements")
