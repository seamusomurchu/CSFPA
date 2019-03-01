#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 12:52:01 2018

@author: james

converts .qb file from mm to m
give full path to file
save to files4CSFPA/Fromabdatio
"""
import numpy as np
import os

outputrep = '/home/james/files4CSFPA/Fromqbdataio/'

def DimensionConvert(filename):
	
	data = np.loadtxt(filename, skiprows=1)
	
	data[:, 2:4] = data[:, 2:4]/1000
	
	print data[0]
	
	#initialise file for saving
	fname = os.path.basename(filename)
	
	with open(outputrep+'mconv_'+fname, 'wb') as f:
		f.write('Xind	Yind 	Ypos	 Xpos	Xamp	 Xpha	Yamp 	Ypha 	Zamp	    Zpha' + '\n')
		np.savetxt(f, data, delimiter='    ',fmt='%17.9e')
	
	#f = open('mconv_'+filename ,'w+')
	
	return