#!/usr/bin/python3
#-*- coding: utf8 -*-

import math

def dist(a, b):
	xdiff = a[0]-b[0]
	ydiff = a[1]-b[1]
	return math.sqrt(xdiff**2 + ydiff**2)


pointfile = open("rawshp/377points.txt", 'r')
points = {}
first = True
for line in pointfile:
	if first:
		first = False
		continue
	elements = line.strip().split(",")
	bfs = elements[1]
	x = int(float(elements[4]))
	y = int(float(elements[5]))
	points[bfs] = (x, y)

distances = {}
for pointA in sorted(points):
	for pointB in sorted(points):
		if pointA == pointB:
			distances[(pointA, pointB)] = 0
		else:
			distances[(pointA, pointB)] = int(dist(points[pointA], points[pointB]))


outfile = open("data/geodist.csv", 'w')
sortedpoints = sorted(points.keys())
outfile.write(";" + ";".join(sortedpoints) + "\n")
for p1 in sortedpoints:
	outfile.write(p1 + ";" + ";".join([str(distances[(p1, p2)]) for p2 in sortedpoints]) + "\n")
