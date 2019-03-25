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
#gqbfile = '/home/james/files4CSFPA/Fromqbdataio/CF1PTDofflinY_CF.qb'
#mfile = '/home/james/Downloads/CS1FP241x241.dat'

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

	xarr = np.asarray(df.X)
	xarr = YvalFixer(df.X)	
	
	mampfilt = df.MagX[xarr == 0.0]
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
	plt.plot(df.Y[xarr == 0.0], mnorm, marker='.', c='r', label="MODAL")
	plt.legend(loc='upper left')
	plt.show()
						   
	return

def GMcuts(mfile, gqbfile, ang):
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
	#setup 45 deg cut data - MODAL
	anglevals = AngledArray(ang, dfg.Xpos)
	
	angmampfilt = df.MagX[dfg.Ypos == anglevals]
	angmnorm = angmampfilt / max(angmampfilt)
	angmnorm = np.asarray(angmnorm)
	angmnorm = 20 * np.log(angmnorm) 
	#45deg GRASP
	anggampfilt = dfg.Xamp[dfg.Ypos == anglevals]
	anggnorm = anggampfilt / max(anggampfilt)
	anggnorm = np.asarray(anggnorm)
	anggnorm = 20 * np.log(anggnorm)
	#initialise plotting
	plt.figure()
	plt.title('0, 90, 45 deg cuts')
	#plot X cut
	plt.plot(dfg.Xpos[dfg.Ypos == 0.0], gnorm, marker='.', label="GRASP X Cut")
	plt.plot(dfg.Xpos[dfg.Ypos == 0.0], mnorm, marker='.', c='r', label="MODAL X Cut")	
	#plot Y cut
	plt.plot(dfg.Ypos[dfg.Xpos == 0.0], ygnorm, marker='.', c='g', label="GRASP Y Cut")
	plt.plot(dfg.Ypos[dfg.Xpos == 0.0], ymnorm, marker='.', c='darkorange', label="MODAL Y Cut")
	#Do 45 deg cut
	plt.plot(dfg.Xpos[dfg.Ypos == anglevals], anggnorm, marker='.', c='mediumspringgreen', label="GRASP 45 deg")
	plt.plot(dfg.Xpos[dfg.Ypos == anglevals], angmnorm, marker='.', c='m', label="MODAL 45 deg")
	#set legend
	plt.legend(loc='lower right')
	plt.show()
	
#	diff = gnorm-mnorm
#	plt.figure()
#	plt.title('difference plot')
#	plt.plot(gnorm-mnorm)
#	plt.show()
						   
	return

def YvalFixer(yarr):
	"""
	takes in array of modal y values and sets small numbers to zero"
	"""
	print type(yarr)
	yarr = np.ma.masked_inside(yarr, -1e-5, 1e-5)
	yarr = np.ma.filled(yarr, fill_value=0.0)
	
			
	return yarr

def AngledArray(ang, arr):
	"""pass in an array of x data, returns corresponding y data
	converts degrees to radians
	might to round float up from +- 59.99999999 to +- 60.0
	NB due to the nature of the input xy data, x value should make sense for the angle
	e.g. if you want an 85 degree cut, make sure the x value is sufficiently small
	"""
	ang = np.deg2rad(ang)
	yarr = arr * np.tan(ang)
	yarr = np.around(yarr, decimals=2)
	return yarr

def GMXangcut(ang, mfile, gqbfile):
	#prep MODAL data
	df = pd.read_csv(mfile, sep='\t', header=0)
	#prep GRASP
	dfg = pd.read_csv(gqbfile, sep='\t', header=0)
	
	dfg.Xpos = dfg.Xpos * 1000 # to get x axis same as modal in mm
	dfg.Ypos = dfg.Ypos * 1000
	
	yarr = np.asarray(df.Y)
	yarr = YvalFixer(df.Y)
	
	anglevals = AngledArray(ang, df.X)
	
	mampfilt = df.MagX[yarr == anglevals]
	mnorm = mampfilt / max(mampfilt)
	mnorm = np.asarray(mnorm)
	mnorm = 20 * np.log(mnorm) 
	
	gampfilt = dfg.Xamp[yarr == anglevals]
	gnorm = gampfilt / max(gampfilt)
	gnorm = np.asarray(gnorm)
	gnorm = 20 * np.log(gnorm)

	plt.figure()
	plt.title('45 deg X cut')
	plt.plot(dfg.Xpos[yarr == anglevals], gnorm, marker='.', label="GRASP")
	plt.plot(df.X[yarr == anglevals], mnorm, marker='.', c='r', label="MODAL")
	plt.legend(loc='upper left')
	plt.show()
						   
	return

def GXangcut(ang, gqbfile):
	#prep GRASP
	dfg = pd.read_csv(gqbfile, sep='\t', header=0)
	
	dfg.Xpos = dfg.Xpos * 1000 # to get x axis same as modal in mm
	dfg.Ypos = dfg.Ypos * 1000
	
	anglevals = AngledArray(ang, dfg.Xpos)
	# angled cut
	gampfilt = dfg.Xamp[dfg.Ypos == anglevals]
	gnorm = gampfilt / max(gampfilt)
	gnorm = np.asarray(gnorm)
	gnorm = 20 * np.log(gnorm)
	# 0 deg cut
	zgampfilt = dfg.Xamp[dfg.Ypos == 0.0]
	zgnorm = zgampfilt / max(zgampfilt)
	zgnorm = np.asarray(zgnorm)
	zgnorm = 20 * np.log(zgnorm)
	#90deg cut
	ygampfilt = dfg.Xamp[dfg.Xpos == 0.0]
	ygnorm = ygampfilt / max(ygampfilt)
	ygnorm = np.asarray(ygnorm)
	ygnorm = 20 * np.log(ygnorm)
	
	plt.figure()
	plt.title('45 deg X cut')
	
	plt.plot(dfg.Xpos[dfg.Ypos == anglevals], gnorm, marker='.', label="GRASP 45 deg")
	plt.plot(dfg.Xpos[dfg.Ypos == anglevals], zgnorm, marker='.', label="GRASP 0 deg")
	plt.plot(dfg.Xpos[dfg.Ypos == anglevals], ygnorm, marker='.', label="GRASP 90 deg")
	
	
	plt.legend(loc='upper left')
	plt.show()
						   
	return
