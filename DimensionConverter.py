#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 12:52:01 2018

@author: james

converts .qb file from mm to m
"""
import numpy as np

def DimensionConvert(filename):
	
	data = np.loadtxt(filename, skiprows=1)
	
	data[:, 2:4] = data[:, 2:4]/1000
	
	print data[0]
	
	with open('mconv_'+filename, 'wb') as f:
		f.write('Xind	Yind 	Ypos	 Xpos	Xamp	 Xpha	Yamp 	Ypha 	Zamp	    Zpha' + '\n')
		np.savetxt(f, data, delimiter='    ',fmt='%17.9e')
	
	#f = open('mconv_'+filename ,'w+')
	
	return