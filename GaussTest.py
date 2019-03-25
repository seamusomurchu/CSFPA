#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 10:27:13 2019

@author: james
test Gaussian fit for a grasp/modal beam
"""
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from cuts import YvalFixer

mfile = '/home/james/Downloads/CS1_861v3.dat'
gqbfile = '/home/james/files4CSFPA/Fromqbdataio/planar_grid_CF_Mstyle.qb'

def GRASPBeamFitter(gqbfile):
	dfg = pd.read_csv(gqbfile, sep='\t', header=0)
	#set x axis to mm
	dfg.Xpos = dfg.Xpos *1000
	#return y vals for gaussian
	gy = Gfunc(dfg.Xpos[dfg.Ypos == 0.0], 0.025, 0, 50, 0)
	popt, pcov = curve_fit(Gfunc, dfg.Xpos[dfg.Ypos == 0.0], dfg.Xamp[dfg.Ypos == 0.0], method='lm', p0=[0.025, 0, 50, 0])
	print "popt = ", popt
	print "pcov = ", pcov
	#do plot
	plt.figure()
	plt.title('GRASP Gaussian Fit')
	plt.plot(dfg.Xpos[dfg.Ypos == 0.0], dfg.Xamp[dfg.Ypos == 0.0], marker='.', label='RAW')
	plt.plot(dfg.Xpos[dfg.Ypos == 0.0], Gfunc(dfg.Xpos[dfg.Ypos == 0.0], *popt), label='Fitted')
	plt.plot(dfg.Xpos[dfg.Ypos == 0.0], gy, label='1st Guess')
#	
#	#2nd guess 
#	gy = Gfunc(dfg.Xpos[dfg.Ypos == 0.0], 590, 0, 25, 0)
#	popt, pcov = curve_fit(Gfunc, dfg.Xpos[dfg.Ypos == 0.0], dfg.Xamp[dfg.Ypos == 0.0], method='lm', p0=[590, 0, 25, 0])
#	plt.plot(dfg.Xpos[dfg.Ypos == 0.0], Gfunc(dfg.Xpos[dfg.Ypos == 0.0], *popt), label='2nd Fitted')
#	plt.plot(dfg.Xpos[dfg.Ypos == 0.0], gy, label='2nd Guess')
#	
#	print "popt = ", popt
#	print "pcov = ", pcov
	
	plt.legend(loc='upper left')
	plt.show()
	return

def MODALBeamFitter(mfile):
	df = pd.read_csv(mfile, sep='\t', header=0)
	#setup yvals for MODAL issue
	yarr = np.asarray(df.Y)
	yarr = YvalFixer(df.Y)
	#return y vals for gaussian
	gy = Gfunc(df.X[yarr == 0.0], 590, 0, 50, 0)
	popt, pcov = curve_fit(Gfunc, df.X[yarr == 0.0], df.MagX[yarr == 0.0], method='lm', p0=[590, 0, 50, 0])
	print "popt = ", popt
	print "pcov = ", pcov
	#do plot
	plt.figure()
	plt.title('MODAL Gaussian Fit')
	plt.plot(df.X[yarr == 0.0], df.MagX[yarr == 0.0], marker='.', label='RAW')
	plt.plot(df.X[yarr == 0.0], Gfunc(df.X[yarr == 0.0], *popt), label='Fitted')
	plt.plot(df.X[yarr == 0.0], gy, label='1st Guess')
	
	#2nd guess 
	gy = Gfunc(df.X[yarr == 0.0], 590, 0, 25, 0)
	popt, pcov = curve_fit(Gfunc, df.X[yarr == 0.0], df.MagX[yarr == 0.0], method='lm', p0=[590, 0, 25, 0])
	plt.plot(df.X[yarr == 0.0], Gfunc(df.X[yarr == 0.0], *popt), label='2nd Fitted')
	plt.plot(df.X[yarr == 0.0], gy, label='2nd Guess')
	
	print "popt = ", popt
	print "pcov = ", pcov
	
	plt.legend(loc='upper left')
	plt.show()
	return

def Gfunc(x, a, c, w, offset):
	return a*np.exp(-((x-c)*(x-c)/(w**2))) + offset