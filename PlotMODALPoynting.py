#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 10:20:12 2019

@author: james
Simple Poynting Plot for MODAL data
"""
import pandas as pd
import matplotlib.pyplot as plt
from CSFPA_dataIO import GetMODALGridPixArea

fpath = '/home/james/Downloads/CS1_250219.dat'
#fpath = '/home/james/Downloads/CS1 0.05 m.dat'
fpath = '/home/james/Downloads/CS1.dat'

def PoynPlot(fpath):
	df = pd.read_csv(fpath, sep='\t', header=0)
	
	garea, parea = GetMODALGridPixArea(fpath)
	
	fig = plt.figure(facecolor='xkcd:pale green')
	fig.suptitle("MODAL Poynting Plot")
	ax = fig.add_subplot(111, facecolor='#d8dcd6')
	sc = ax.scatter(df.X, df.Y, c=df.PoynZ*parea, cmap='jet', marker='.')
	cbar = fig.colorbar(sc, label="MODAL Poynting (W)")
	
	#calculate poynting from .dat
	P = (df.MagX*np.cos(df.PhaseX)**2 + df.MagX*np.sin(df.PhaseX)**2) + (df.MagY*np.cos(df.PhaseY)**2 + df.MagY*np.sin(df.PhaseY)**2)
	#calcualte sum of power
	print "Poynting Sum W = ", sum(df.PoynZ*parea)
	return