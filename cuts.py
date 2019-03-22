#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 17:07:27 2019

@author: james
cuts version
"""
import pandas as pd
import matplotlib.pyplot as plt
mfile = '/home/james/Downloads/CS1_861v3.dat'
gqbfile = '/home/james/files4CSFPA/Fromqbdataio/planar_grid_CF_Mstyle.qb'
def GMcuts(mfile, gqbfile):
	#prep MODAL data
	df = pd.read_csv(mfile, sep='\t', header=0)
	#prep GRASP
	dfg = pd.read_csv(gqbfile, sep='\t', header=0)
	
	dfg.Xpos = dfg.Xpos * 1000 # to get x axis same as modal in mm
	dfg.Ypos = dfg.Ypos * 1000
	
	mampfilt = df.MagX[df.Y == -0.5]
	mnorm = mampfilt / max(mampfilt)
	
	gampfilt = dfg.Xamp[dfg.Ypos == -0.5]
	gnorm = gampfilt / max(gampfilt)

	plt.figure()
	plt.plot(dfg.Xpos[dfg.Ypos == -0.5], gnorm, marker='.')
	plt.plot(df.X[df.Y == -0.5], mnorm, marker='.', c='r')
	plt.show()
	
					   
	return

