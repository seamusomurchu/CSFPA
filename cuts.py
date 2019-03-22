#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 17:07:27 2019

@author: james
cuts version
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
mfile = '/home/james/Downloads/CS1_861v3.dat'
gqbfile = '/home/james/files4CSFPA/Fromqbdataio/planar_grid_CF_Mstyle.qb'
mfile = '/home/james/Downloads/CS1_861.dat'
gqbfile = '/home/james/files4CSFPA/Fromqbdataio/FPLinX_Mstyle.qb'
def GMXcut(mfile, gqbfile):
	#prep MODAL data
	df = pd.read_csv(mfile, sep='\t', header=0)
	#prep GRASP
	dfg = pd.read_csv(gqbfile, sep='\t', header=0)
	
	dfg.Xpos = dfg.Xpos * 1000 # to get x axis same as modal in mm
	dfg.Ypos = dfg.Ypos * 1000
	
	yarr = np.asarray(df.Y)
	yarr = YvalFixer(df.Y)
	
	mampfilt = df.MagX[yarr == 0.0]
	mnorm = mampfilt / max(mampfilt)
	mnorm = np.asarray(mnorm)
	mnorm = 20 * np.log(mnorm) 
	
	gampfilt = dfg.Xamp[dfg.Ypos == 0.0]
	gnorm = gampfilt / max(gampfilt)
	gnorm = np.asarray(gnorm)
	gnorm = 20 * np.log(gnorm)

	plt.figure()
	plt.title('X cut')
	plt.plot(dfg.Xpos[dfg.Ypos == 0.0], gnorm, marker='.', label="GRASP")
	plt.plot(df.X[yarr == 0.0], mnorm, marker='.', c='r', label="MODAL")
	plt.legend(loc='upper left')
	plt.show()
						   
	return

def GMYcut(mfile, gqbfile):
	#prep MODAL data
	df = pd.read_csv(mfile, sep='\t', header=0)
	#prep GRASP
	dfg = pd.read_csv(gqbfile, sep='\t', header=0)
	
	dfg.Xpos = dfg.Xpos * 1000 # to get x axis same as modal in mm
	dfg.Ypos = dfg.Ypos * 1000
	
	
	mampfilt = df.MagX[df.X == 0.0]
	mnorm = mampfilt / max(mampfilt)
	mnorm = np.asarray(mnorm)
	mnorm = 20 * np.log(mnorm) 
	
	gampfilt = dfg.Xamp[dfg.Xpos == 0.0]
	gnorm = gampfilt / max(gampfilt)
	gnorm = np.asarray(gnorm)
	gnorm = 20 * np.log(gnorm)

	plt.figure()
	plt.title('Y cut')
	plt.plot(dfg.Ypos[dfg.Xpos == 0.0], gnorm, marker='.', label="GRASP")
	plt.plot(df.Y[df.X == 0.0], mnorm, marker='.', c='r', label="MODAL")
	plt.legend(loc='upper left')
	plt.show()
						   
	return
def GMcuts(mfile, gqbfile):
	#prep MODAL data
	df = pd.read_csv(mfile, sep='\t', header=0)
	#prep GRASP
	dfg = pd.read_csv(gqbfile, sep='\t', header=0)
	#convert grasp to mm
	dfg.Xpos = dfg.Xpos * 1000 # to get x axis same as modal in mm
	dfg.Ypos = dfg.Ypos * 1000
	
	#setup Y values
	xarr = np.asarray(df.X)
	xarr = YvalFixer(df.X)
	#normliase and log mag data
	Ycutmampfilt = df.MagX[xarr == 0.0]
	ymnorm = Ycutmampfilt / max(Ycutmampfilt)
	ymnorm = np.asarray(ymnorm)
	ymnorm = 20 * np.log(ymnorm) 
	
	Ycutgampfilt = dfg.Xamp[dfg.Xpos == 0.0]
	ygnorm = Ycutgampfilt / max(Ycutgampfilt)
	ygnorm = np.asarray(ygnorm)
	ygnorm = 20 * np.log(ygnorm)

	#setup X values
	yarr = np.asarray(df.Y)
	yarr = YvalFixer(df.Y)
	
	mampfilt = df.MagX[yarr == 0.0]
	mnorm = mampfilt / max(mampfilt)
	mnorm = np.asarray(mnorm)
	mnorm = 20 * np.log(mnorm) 
	
	gampfilt = dfg.Xamp[dfg.Ypos == 0.0]
	gnorm = gampfilt / max(gampfilt)
	gnorm = np.asarray(gnorm)
	gnorm = 20 * np.log(gnorm)	

	plt.figure()
	plt.title('X and Y Cuts')
	#plot X cut
	plt.plot(dfg.Xpos[dfg.Ypos == 0.0], gnorm, marker='.', label="GRASP X Cut")
	plt.plot(dfg.Xpos[dfg.Ypos == 0.0], mnorm, marker='.', c='r', label="MODAL X Cut")	
	#plot Y cut
	plt.plot(dfg.Xpos[dfg.Ypos == 0.0], ygnorm, marker='.', c='g', label="GRASP Y Cut")
	plt.plot(dfg.Xpos[dfg.Ypos == 0.0], ymnorm, marker='.', c='darkorange', label="MODAL Y Cut")
	
	plt.legend(loc='upper left')
	plt.show()
						   
	return

def YvalFixer(yarr):
	"""
	takes in array of modal y values and sets small numbers to zero"
	"""
	print type(yarr)
	yarr = np.ma.masked_inside(yarr, -1e-5, 1e-5)
	yarr = np.ma.filled(yarr, fill_value=0.0)
	
			
	return yarr

