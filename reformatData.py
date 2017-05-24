#! /usr/bin/python3
# -*- coding: utf-8 -*-

import glob, re

for infilename in glob.glob("origdata/BFS_*.csv"):
	infile = open(infilename, 'r')
	outfilename = re.sub(r'BFS_68phen_(\d)Gr_(.)\w+', r'\1\2', infilename)
	outfilename = outfilename.replace("origdata", "data")
	print(infilename, "=>", outfilename)
	outfile = open(outfilename, 'w')
	for line in infile:
		if line.replace(";", "").strip() == "":
			continue
		line = line.replace(",", ".").replace(";", ",")
		outfile.write(line)
	infile.close()
	outfile.close()
