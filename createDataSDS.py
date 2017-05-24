#!/usr/bin/python
#-*- coding: iso-8859-1 -*-

import arcpy, os, re, codecs


sds2bfs = {}
numberfile = "rawshp/378_Orte_VDM_ID.txt"
first = True
nf = open(numberfile)
for line in nf:
	if first:
		first = False
		continue
	elements = line.strip().split(",")
	sds2bfs[elements[6]] = elements[3]
del sds2bfs["AG54"]		# Menziken, not in SADS data set

data = {}
maps = []


## V2 ##

allfeatsfolder = "C:/Users/yves/Desktop/these/cartes-dialectes/sds-v2-allfeats/"
virtualmaps = (u"2095_lich", u"3001_schwa_eä", u"3001_schwa_eäa", u"3056ff_kommen_inf_pp", u"3092_nehmen_1sg", u"3100_kommen_1sg", u"3107_mögen_13pl", u"3108_dürfen_pl", u"3217_unser_MN_Dat")
# V2 maps that should be replaced by updated V3 maps
updatedmaps = (u"1035_eng", u"1054_1055_Rücken", u"2003ff_Schnabel", u"4150_als", u"4155_ein_wenig", u"6026_immer")

for variableFile in os.listdir(allfeatsfolder):
	if not variableFile.endswith(".shp"):
		continue
		
	print variableFile
	if variableFile.replace(".shp", "").decode('iso-8859-1') in virtualmaps:
		print "=> SKIP (virtual)"
		continue
	if variableFile.replace(".shp", "").decode('iso-8859-1') in updatedmaps:
		print "=> SKIP (updated)"
		continue
	
	mapname = variableFile.replace(".shp", "").decode('iso-8859-1')
	maps.append(mapname)
	
	variants = []
	fieldList = arcpy.ListFields(allfeatsfolder + variableFile, "cnt_*")
	for field in fieldList:
		if field.baseName != "cnt_total":
			variants.append(field.baseName.replace("cnt_", ""))
	
	rowList = arcpy.SearchCursor(allfeatsfolder + variableFile)
	for row in rowList:
		if row.SDS_CODE not in sds2bfs:		# only keep places that are in the SDS-SADS intersection
			continue
		loc = sds2bfs[row.SDS_CODE]
		if loc not in data:
			data[loc] = {}
		if mapname not in data[loc]:
			data[loc][mapname] = []
		for variant in variants:
			fieldvalue = int(row.getValue("cnt_" + variant))
			if fieldvalue >= 1:		# there are two maps (2071 and 2093) where cnt values can be higher than one
				data[loc][mapname].append(variant)


## V3 ##

removemaps = ("1_062_Abend", )
gdb = "C:/Users/yves/Desktop/these/cartes-dialectes/RoyWeiss/Template_SDS.gdb"
arcpy.env.workspace = gdb
for variableFile in arcpy.ListFeatureClasses():
	if variableFile.startswith("SDS_Template"):
		continue
	mapname = variableFile[4:]
	print mapname
	if mapname in removemaps:
		print "=> SKIP (remove)"
		continue
	
	maps.append(mapname)
	variants = []
	fieldList = arcpy.ListFields(gdb + "/" + variableFile, "cnt_*")
	for field in fieldList:
		if (field.baseName != "cnt_total") and (field.baseName != "cnt_primary"):
			variants.append(field.baseName.replace("cnt_", ""))
	
	rowList = arcpy.SearchCursor(gdb + "/" + variableFile)
	for row in rowList:
		if row.SDS_CODE not in sds2bfs:		# only keep places that are in the SDS-SADS intersection
			continue
		loc = sds2bfs[row.SDS_CODE]
		if loc not in data:
			data[loc] = {}
		if mapname not in data[loc]:
			data[loc][mapname] = []
		for variant in variants:
			fieldvalue = int(row.getValue("cnt_" + variant))
			if fieldvalue == 1:
				data[loc][mapname].append(variant)


def writeData(maps, data, outfilename, mapSelection=lambda x: True):
	ofile = codecs.open(outfilename, 'w', encoding='iso-8859-1')
	line1 = ["LOC"] + [m for m in maps if mapSelection(m)]
	line2 = ";".join(line1)
	ofile.write(line2 + "\r\n")
	for loc in sorted(data):
		line1 = [loc]
		for m in maps:
			if mapSelection(m):
				if (loc not in data) or (m not in data[loc]):
					line1.append("")
				else:
					line1.append("|".join(data[loc][m]))
		line2 = ";".join(line1)
		ofile.write(line2 + "\r\n")
	ofile.close()


writeData(maps, data, "data/sds-all.csv")
writeData(maps, data, "data/sds-phon.csv", lambda x: x[0] in "12")
writeData(maps, data, "data/sds-morph.csv", lambda x: x[0] == "3")
writeData(maps, data, "data/sds-lex.csv", lambda x: x[0] in "45678")
