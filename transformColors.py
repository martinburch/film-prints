#!/usr/bin/env python
# encoding: utf-8

"""
transformColors.py

Changes colors from RGB to polar coordinates. Feed it JSON files. Output: CSV, of course

"""

import json
import urllib2
import csv
import numpy as np

def dictListToFile(dictrows, filename, fieldnames, delimiter='\t',
          lineterminator='\n'):
	out = open(filename, 'w')
	
	# Write out header
	header = delimiter.join(fieldnames) + lineterminator
	out.write(header)
	
	# Write out dictionary
	data = csv.DictWriter(out, fieldnames,
	          delimiter=delimiter,
	          lineterminator=lineterminator)
	data.writerows(dictrows)
	out.close()

movieList = ["Argo","Beasts_of_the_Southern_Wild","Django_Unchained","Les_Miserables","Life_of_Pi","Lincoln","Silver_Linings_Playbook","Zero_Dark_Thirty"]

for movie in movieList:
	url = "http://roadtolarissa.com/film-strips/movieStills/%s/colors.json" % (movie)
	response = urllib2.urlopen(url)
	data = response.read()
	jsonData = json.loads(data)
	for idx,item in enumerate(jsonData):
		rgb = item['rgb']
		# split string into list on commas and cast to ints via list comprehension
		r,g,b = [ float(x) for x in rgb.split(',') ]
		
		r = r / 255
		g = g / 255
		b = b / 255
		
		maxRGB = 0.0
		minRGB = 0.0
		
		maxRGB = max([r,g,b])
		minRGB = min([r,g,b])
		
		c = 0.0
		
		c = maxRGB - minRGB
		
		h = 0.0
		
		if c == 0:
			h = 0.0
		elif maxRGB == r:
			h = ((g - b) / c) % 6
		elif maxRGB == g:
			h = ((b - r) / c) + 2
		elif maxRGB == b:
			h = ((r - g) / c) + 4
		else:
			raise Exception("unable to determine hue")
			
		h = 60*h
		
		theta = h * (np.pi / 180)
		
		# write data back to object
		jsonData[idx]['r'] = r
		jsonData[idx]['g'] = g
		jsonData[idx]['b'] = b
		jsonData[idx]['maxRGB'] = maxRGB
		jsonData[idx]['minRGB'] = minRGB
		jsonData[idx]['c'] = c		
		jsonData[idx]['h'] = h
		jsonData[idx]['theta'] = theta
	
	dictListToFile(jsonData, movie+'.csv', ["i","rgb","r","g","b","maxRGB","minRGB","c","h","theta"])