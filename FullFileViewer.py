#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 11:55:15 2019

@author: james
Take a GRASP or possibly MODAL in future
"""
import os
import matplotlib.pyplot as plt
import pandas as pd
from CSFPA_dataIO import GridPowerCalc
import numpy as np

#gqbfile = '/home/james/files4CSFPA/Fromqbdataio/CF1linx_CF.qb'
#gpath = '/home/james/files4CSFPA/qbdataioOUTFILES/FPA_objs_CF1linx_CF.qb.pkl'
#gqbfile = '/home/james/files4CSFPA/Fromqbdataio/CF1PTDofflinY_CF.qb'
#gpath = '/home/james/files4CSFPA/qbdataioOUTFILES/FPA_objs_CF1PTDofflinY_CF.qb.pkl'
gqbfile = '/home/james/files4CSFPA/Fromqbdataio/CF1PTDofflinY_Mstyle.qb'
gpath = '/home/james/files4CSFPA/qbdataioOUTFILES/FPA_objs_CF1PTDofflinY_Mstyle.qb.pkl'


def FullFileView(gqbfile, gpath):
	#load file
	df = pd.read_csv(gqbfile, sep='\t', header=0)
	#load pkl, and calculate normalised power from total intensity
	gfile = os.path.basename(gpath)
	GPow = GridPowerCalc(gfile)	
	#make figure
	fig = plt.figure(facecolor='xkcd:pale green')
	fig.suptitle("Full View of Data")	
	#MagX plot
	ax1 = fig.add_subplot(241, facecolor='#d8dcd6', aspect='equal')
	ax1.set_title("Magnitude X")					   
   	sc = ax1.scatter(df.Xpos, df.Ypos, c=df.Xamp, cmap='jet', marker='.')
	cbar = fig.colorbar(sc, label="Mag X")
	#MagY plot
	ax2 = fig.add_subplot(242, facecolor='#d8dcd6', aspect='equal')
	ax2.set_title("Magnitude Y")					   
	sc = ax2.scatter(df.Xpos, df.Ypos, c=df.Yamp, cmap='jet', marker='.')	
	cbar = fig.colorbar(sc, label="Mag Y")					   
	#Xphase
	ax3 = fig.add_subplot(243, facecolor='#d8dcd6', aspect='equal')
	ax3.set_title("Phase X")					   
	sc = ax3.scatter(df.Xpos, df.Ypos, c=df.Xpha, cmap='jet', marker='.')	
	cbar = fig.colorbar(sc, label="Phase X")	  
	#yphase
	ax4 = fig.add_subplot(244, facecolor='#d8dcd6', aspect='equal')
	ax4.set_title("Phase Y")					   
	sc = ax4.scatter(df.Xpos, df.Ypos, c=df.Ypha, cmap='jet', marker='.')	
	cbar = fig.colorbar(sc, label="Phase Y")
	#Zamp
	ax5 = fig.add_subplot(245, facecolor='#d8dcd6', aspect='equal')
	ax5.set_title("Magnitude Z")					   
	sc = ax5.scatter(df.Xpos, df.Ypos, c=df.Zamp, cmap='jet', marker='.')	
	cbar = fig.colorbar(sc, label="Mag Z")
	#zphase
	ax6 = fig.add_subplot(246, facecolor='#d8dcd6', aspect='equal')
	ax6.set_title("Phase Z")					   
	sc = ax6.scatter(df.Xpos, df.Ypos, c=df.Zpha, cmap='jet', marker='.')	
	cbar = fig.colorbar(sc, label="Phase Z")
	#normalised total intensity	 
	ax7 = fig.add_subplot(247, facecolor='#d8dcd6', aspect='equal')
	ax7.set_title("Total Intensity")					   
	sc = ax7.scatter(df.Xpos, df.Ypos, c=GPow, cmap='jet', marker='.')	
	cbar = fig.colorbar(sc, label="Watts")	
   	return