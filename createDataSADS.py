#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os, csv, re, codecs, sys


validbfs = set()
numberfile = "rawshp/378_Orte_VDM_ID.txt"
print("Loading valid set of data points from", numberfile)
first = True
nf = open(numberfile)
for line in nf:
	if first:
		first = False
		continue
	elements = line.strip().split(",")
	validbfs.add(elements[3])
	

def createData(infilename, outfilename):
	print("Converting", infilename, "to", outfilename)
	maps = []
	columns2variants = {}
	csvreader = csv.reader(open(infilename, 'r'), delimiter="\t")
	csvwriter = csv.writer(open(outfilename, 'w'), delimiter=";")
	header = True
	for row in csvreader:
		if header:
			for i, column in enumerate(row[1:]):
				if column.startswith("cl"):
					continue
				variable, variant = column.split("_", 1)
				if variable not in maps:
					maps.append(variable)
				columns2variants[i+1] = (variable, variant)
			headerrow = ["LOC"] + maps
			csvwriter.writerow(headerrow)
			header = False
		
		else:
			bfsid = row[0].strip()
			if bfsid not in validbfs:
				print("Skip location:", bfsid)
				continue
			data = {}
			for i, value in enumerate(row[1:]):
				value = int(float(value))
				if value == 1:
					if i+1 in columns2variants:
						variable, variant = columns2variants[i+1]
						if variable in data:
							data[variable] += "|" + variant
						else:
							data[variable] = variant
			datarow = [bfsid]
			for m in maps:
				if m in data:
					datarow.append(data[m])
				else:
					datarow.append("")
			csvwriter.writerow(datarow)


# prozente.txt not used yet
data = {"all68_ex.txt": "sads-68ex.csv", "all68_over30.txt": "sads-68over30.csv", "all68_over40.txt": "sads-68over40.csv", "all68_over50.txt": "sads-68over50.csv", "all68_dom_bereinigt.txt": "sads-68dom.csv"}

for f in data:
	createData("/home/yves/dropbox/Dialektometrie/Tabellen/" + f, "data/" + data[f])


def createPercentageData(infilename, outfilename):
	print("Converting", infilename, "to", outfilename)
	maps = []
	columns2variants = {}
	csvreader = csv.reader(open(infilename, 'r'), delimiter="\t")
	csvwriter = csv.writer(open(outfilename, 'w'), delimiter=";")
	header = True
	for row in csvreader:
		if header:
			csvwriter.writerow(["LOC"] + row[1:])
			header = False
		else:
			bfsid = row[0].strip()
			if bfsid not in validbfs:
				print("Skip location:", bfsid)
			else:
				csvwriter.writerow(row)

createPercentageData("/home/yves/dropbox/Dialektometrie/Tabellen/all68_prozente.txt", "data/sads-68pro.csv")

