#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 11:59:03 2019

@author: james
NB grasp manual 1113 describes x cycles faster than y. For each Y, it cycles through X.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from qbdataio import getgraspinfo

path = '/home/james/Downloads/CF1PTDofflinY.grd'
#path = '/home/james/Downloads/CF1linx.grd'

def scatplot(path):
		#fname = os.path.basename(path)
	freq, dims, pdims, ktype, params, ixiyparam, datastart = getgraspinfo(path)
	
	nx = pdims[0]	
	ny = pdims[1]

	xmin = dims[0]
	xmax = dims[2]
	ymin = dims[1]
	ymax = dims[3]

	xx = np.linspace(xmin,xmax,nx)
	yy = np.linspace(ymin,ymax,ny)
	
	X,Y = np.meshgrid(xx,yy)
	pts = np.c_[X.ravel(),Y.ravel()]
	Ypt = pts[:,1]
	Xpt = pts[:,0]
	
	data = np.loadtxt(path, skiprows=datastart)
	TotI = (data[:,0]**2 + data[:,1]**2) + (data[:,2]**2 + data[:,4]**2)
	
	fig = plt.figure(facecolor='xkcd:pale green')	
	ax1 = fig.add_subplot(111, facecolor='#d8dcd6', aspect='equal')
	ax1.set_title("Total Intensity from grd")					   
   	sc = ax1.scatter(Xpt, Ypt, c=TotI, cmap='jet', marker='.')
	cbar = fig.colorbar(sc, label="Total Intensity")
	
	return

def meshplot(path):
	
	#fname = os.path.basename(path)
	freq, dims, pdims, ktype, params, ixiyparam, datastart = getgraspinfo(path)
	
	nx = pdims[0]	
	ny = pdims[1]

	xmin = dims[0]
	xmax = dims[2]
	ymin = dims[1]
	ymax = dims[3]

	xx = np.linspace(xmin,xmax,nx)
	yy = np.linspace(ymin,ymax,ny)
	
	X,Y = np.meshgrid(xx,yy)
	data = np.loadtxt(path, skiprows=12)
	Z = (data[:,0]**2 + data[:,1]**2) + (data[:,2]**2 + data[:,4]**2)
	Z = Z.reshape(X.shape)
	plt.contourf(X, Y, Z,100 )
	return pts