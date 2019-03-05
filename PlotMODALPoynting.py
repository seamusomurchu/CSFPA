#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 10:20:12 2019

@author: james
Simple Poynting Plot for MODAL data
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from CSFPA_dataIO import GetMODALGridPixArea, GridPowerCalc, RetrieveVars

mpath = '/home/james/Downloads/CS1_250219.dat'
#fpath = '/home/james/Downloads/CS1 0.05 m.dat'

#mpath = '/home/james/Downloads/CS1.dat'
gpath = '/home/james/files4CSFPA/qbdataioOUTFILES/FPA_objs_CF1PTDofflinY_CF.qb.pkl'
gfile = 'FPA_objs_CF1PTDofflinY_CF.qb.pkl'

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

def PoynICompPlot(mpath, gpath):
	#prep MODAL data
	df = pd.read_csv(mpath, sep='\t', header=0)
	garea, parea = GetMODALGridPixArea(mpath)
	#prep GRASP
	MagXarr, PhaXarr, ReXarr, ImXarr, MagYarr, PhaYarr, ReYarr, ImYarr, vtxcntarr, PixCenX, PixCenY, IntX, IntY, IntT, Ix, Iy, IT, xycoords, filename = RetrieveVars(gpath)
	gfile = os.path.basename(gpath)
	GPow = GridPowerCalc(gfile)
	#calculate %diff
	comp = ((df.PoynZ*parea - GPow) / GPow) * 100
	fourpi = 4*np.pi
	#do multi plots
	fig = plt.figure(facecolor='xkcd:pale green')
	fig.suptitle("FP Comparison")
	
	ax1 = fig.add_subplot(221, facecolor='#d8dcd6')
	ax1.set_title("MODAL FP from Poynting Z")					   
   	sc = ax1.scatter(df.X, df.Y, c=df.PoynZ*parea/fourpi, cmap='jet', marker='.')
	cbar = fig.colorbar(sc, label="MODAL Poynting (W)")
	
	ax2 = fig.add_subplot(222, facecolor='#d8dcd6')
	ax2.set_title("GRASP FP from Total Intensity")					   
	sc = ax2.scatter(xycoords[:,0],xycoords[:,1], c=GPow, cmap='jet', marker='.')	
	cbar = fig.colorbar(sc, label="GRASP Total Intensity (W)")	
	#plot %diff between models
	ax3 = fig.add_subplot(212, facecolor='#d8dcd6', aspect='equal')
	ax3.set_title("% Difference between Softwares")	
	sc = ax3.scatter(xycoords[:,0],xycoords[:,1], c=comp, cmap='RdPu', marker='.')
	cbar = fig.colorbar(sc, label="% Difference")				            
   #calcualte sum of power
	print "Poynting Sum W = ", sum(df.PoynZ*parea), "% Diff from 4pi = ", ((sum(df.PoynZ*parea)- fourpi) / fourpi) * 100
	return