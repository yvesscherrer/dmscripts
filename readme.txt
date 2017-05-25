1. Vollständige Feature-Matrix (Geoling-Format)
	=> Auswahl von Kartentiteln (und ggf. von Ortspunkten)
2. Ausgewählte Feature-Matrix (Geoling-Format)
	=> Auswahl eines Distanzmasses (RIW, Hamming, ...)
3. Distanzmatrix
	=> Auswahl eines Aggregationsmasses (Min, Max, Schiefe, geogr. Korrelation)
4. Wertematrix
	=> Auswahl eines Klassifizierungsalgorithmus + Anzahl Klassen (MINMWMAX, MEDMW)
5. Klassenmatrix



Schritte:

- createDataSDS.py [Windows] -> liest SHP und GDB aus und erstellt Datenmatrix [>data]
- createDataSADS.py [Linux] -> konvertiert Philipp's CSV-Files [>data]
- createGeoDistanceMatrix.py [Linux] -> berechnet geografische (euklidische) Distanzen zwischen Ortspunktpaaren [>data]
- experiment.py [Linux] -> berechnet Wertetabelle aus Datenmatrizen [<data, >csv]
- visualise.py [Windows] -> konvertiert CSV-Files in Shapefiles und Shapefiles in Layerfiles und exportiert sie als PDF oder PNG [<csv, >shp, >lyr, >png, >pdf]


YS 16.6.15

Daten regeneriert nach Korrektur eines Koordinatenfehlers 23.8.2016:
- rawshp/*
- geodist.csv
- geo-correl-*.csv
- similarity_measures.txt
- *.shp
- *.png

YS 25.5.2017: alles regeneriert mit neuen Skripts (kleine Veränderungen in den US-Klassen, aber wir haben ja eh die Values genommen...)
