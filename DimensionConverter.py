#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 12:52:01 2018

@author: james

converts .qb file from mm to m
"""
import numpy as np

inputrep = '/home/james/files4CSFPA/Fromqbdataio/'

def DimensionConvert(filename):
	
	data = np.loadtxt(inputrep+filename, skiprows=1)
	
	data[:, 2:4] = data[:, 2:4]/1000
	
	print data[0]
	
	with open(inputrep+'mconv_'+filename, 'wb') as f:
		f.write('Xind	Yind 	Ypos	 Xpos	Xamp	 Xpha	Yamp 	Ypha 	Zamp	    Zpha' + '\n')
		np.savetxt(f, data, delimiter='    ',fmt='%17.9e')
	
	#f = open('mconv_'+filename ,'w+')
	
	return