#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 12:51:58 2019

@author: james
multi frequency analysis code similar to qbdataio but now included in CSFPA
"""

import numpy as np
import pandas as pd
import glob

def MultiGraspInfo(fname):
	#load frequencies
	freqs = np.loadtxt('FrequencyListGHz.txt', delimiter=',')
	#load file with multiple frequencies
	infile = open(fname,'r')
	#prob bad coding but use anyway. won't work for large number of frequencies
	freqindex = 100
	iktype = 100
	iparams = 100
	ixiy_index = 100
	GRASPgridarea = 100
	GRASPpixels = 100
	datastart = 100
	for i in range(100):
		temp = infile.readline()
		#print i, temp
		
		if '++++' in temp:			#this line catches the end of header by finding '++++'
			print 'found +++', i
			GRASPgridarea = i + 3 + len(freqs)
			GRASPpixels = i + 4 + len(freqs)
			datastart = i + 5 + len(freqs)
			
		if i == GRASPgridarea:		#sets grid area into array
			gridarea = temp 
			print gridarea                
			dims = [float(s) for s in gridarea.split()]
			dims = np.asarray(dims)
			print dims[0],dims[2]
		if i == GRASPpixels:
			gpix = temp
			pdims = [float(s) for s in gpix.split()]
			pdims = np.asarray(pdims)		
	
	return dims, pdims, datastart

def FreqSplitter(filename, pdims):
	#this program takes a multi frequency grasp file and...,
	#splits it into single frequency files
	#set temp outfile
	outrep = "/home/james/files4CSFPA/freqfiles/"
	outfile = "/home/james/files4CSFPA/tempfiles/tempMultiF.txt"
	freqs = np.loadtxt('FrequencyListGHz.txt', delimiter=',')
	with open(filename) as f:
	    with open(outfile, "w") as f1:
	        for line in f:
	            if len(line.split()) == 6:
	                f1.write(line)
	#initialise reading arrays
	l1 = np.linspace(0, pdims[0]**2*len(freqs), len(freqs)+1)
	l2 = np.linspace(pdims[0]**2, pdims[0]**2*len(freqs), len(freqs))
	#load load temp file as pandas array/DF
	df = pd.read_csv("/home/james/files4CSFPA/tempfiles/tempMultiF.txt", sep='\s+', header=None)
	#XXX
	i = 0	
	for i, freq in enumerate(freqs):
		print freq, i
		f = open(outrep+'FreqFile'+str(freq)+'.qbsf', "w")	#qbsf, sf => single frequency file
		#print df[int(l1[i]):int(l2[i])]
		dft = df[int(l1[i]):int(l2[i])]
		dft.to_csv(f, sep=',', index=False, header=False, float_format='%.9e')
		
	return

def FileConverter():
	"""
	this function will search for single frequency files and convert them to
	modal style file format by calling qbdataio &
	output them in a folder 
	which will then be used by CSFPA_main
	"""
	
	return

def MultiFreqMain(filename):
	#get raw info from grasp file
	dims, pdims, datastart = MultiGraspInfo(filename)
	#make temp file in split frequency files
	FreqSplitter(filename, pdims)
	#use single frequency files and sum them into a new file
	FreqSummer()
	"""
	this will take the shape of looping over tempfile for the number of lines
	for each frequency (use pdims var to initialise an array for this)
	
	"""
	
	return

def FreqSummer():
	"""
	I should actually sum intensities here nor Re&Im - return to later
	
	this function should take/find the individual frequency files and
	sum each value in each row
	keep in mind each file has a total power of 4pi
	"""
	#outrep really should be global init
	outrep = "/home/james/files4CSFPA/freqfiles/"
	#create list of single frequency files
	filelist = glob.glob(outrep + '*.qb')
	#create empty array to loop over using file shape
	lfile = np.loadtxt(filelist[0], delimiter=',', skiprows=0)
	temparr = np.array([lfile.shape])
	#loop over files with index
	for i, fname in enumerate(filelist[1:]):
		lfile = np.loadtxt(fname, delimiter=',', skiprows=0)
		print "load file shape, ", lfile.shape
		temparr = np.hstack((temparr, lfile))
	
	return
