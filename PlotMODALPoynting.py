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

mpath = '/home/james/Downloads/CS1FP241x241.dat'
#mpath = '/home/james/Downloads/CS1_250219.dat'
#mpath = '/home/james/Downloads/CS1 0.05 m.dat'
#mpath = '/home/james/Downloads/CS18319.dat'
#mpath = '/home/james/Downloads/CS1_cal.dat'
#mpath = '/home/james/Downloads/CS1.dat'
#gpath = '/home/james/files4CSFPA/qbdataioOUTFILES/FPA_objs_CF1PTDofflinY_CF.qb.pkl'
#gfile = 'FPA_objs_CF1PTDofflinY_CF.qb.pkl'
#gpath = '/home/james/files4CSFPA/qbdataioOUTFILES/FPA_objs_CFtestLinX05m_CF.qb.pkl'
#gfile = 'FPA_objs_CFtestLinX05m_CF.qb.pkl'
#gpath = '/home/james/files4CSFPA/qbdataioOUTFILES/FPA_objs_CFtest_CF.qb.pkl'
#gfile = 'FPA_objs_CFtest_CF.qb.pkl'
gqbfile = '/home/james/files4CSFPA/Fromqbdataio/CF1linx_CF.qb'
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
	
	ax1 = fig.add_subplot(221, facecolor='#d8dcd6', aspect='equal')
	ax1.set_title("MODAL FP from Poynting Z")					   
   	sc = ax1.scatter(df.X, df.Y, c=df.PoynZ*parea, cmap='jet', marker='.')
	cbar = fig.colorbar(sc, label="MODAL Poynting (W)")
	
	ax2 = fig.add_subplot(222, facecolor='#d8dcd6', aspect='equal')
	ax2.set_title("GRASP FP from Total Intensity")					   
	sc = ax2.scatter(xycoords[:,0]*1000, xycoords[:,1]*1000, c=GPow, cmap='jet', marker='.')	
	cbar = fig.colorbar(sc, label="GRASP Total Intensity (W)")	
	#plot %diff between models
	ax3 = fig.add_subplot(223, facecolor='#d8dcd6', aspect='equal')
	ax3.set_title("% Difference between Softwares")	
	sc = ax3.scatter(xycoords[:,0]*1000, xycoords[:,1]*1000, c=comp, cmap='PiYG', marker='.') #Both useful PiYG & RdPu
	cbar = fig.colorbar(sc, label="% Difference")	
#plot histogram of %diff per pixel
	ax4 = fig.add_subplot(224, facecolor='#d8dcd6')	
	ax4.set_title("% Difference Histogram")
	n, bins, patches = ax4.hist(comp)
	print "hist data", n, bins, patches			            
   #calcualte sum of power
	print "Poynting Sum W = ", sum(df.PoynZ*parea), "% Diff from 1 W = ", ((sum(df.PoynZ*parea) - 1) / 1) * 100
	return

def MagXCompPlot(mpath, gqbfile):
	#prep MODAL data
	df = pd.read_csv(mpath, sep='\t', header=0)
	garea, parea = GetMODALGridPixArea(mpath)
	#MagXY = df.MagX.add(df.MagY, fill_value=0) will give intensity pattern
	#prep GRASP
	dfg = pd.read_csv(gqbfile, sep='\t', header=0)
	#Do Plot
	fig = plt.figure(facecolor='xkcd:pale green')
	fig.suptitle("FP MagX Comparison")
	
	ax1 = fig.add_subplot(221, facecolor='#d8dcd6', aspect='equal')
	ax1.set_title("MODAL FP Magnitude X")					   
   	sc = ax1.scatter(df.X, df.Y, c=df.MagX, cmap='jet', marker='.')
	cbar = fig.colorbar(sc, label="MagX")	
	
	ax2 = fig.add_subplot(222, facecolor='#d8dcd6', aspect='equal')
	ax2.set_title("GRASP FP MagX (qbfile)")					   
	sc = ax2.scatter(dfg.Xpos*1000, dfg.Ypos*1000, c=dfg.Yamp, cmap='jet', marker='.')	
	cbar = fig.colorbar(sc, label="GRASP X Amp")	
	
	return