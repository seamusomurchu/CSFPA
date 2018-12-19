#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 12:01:08 2018

@author: james

copied version of Creidhes plotter
"""
# %cd "C:\Users\Creidhe\Documents\OneDrive - Maynooth University\Work\My Research\Graduate Students\James M 2017 -"
import numpy as np
import scipy
import matplotlib.pyplot as plt

#takes in grasp file and grasp datasize e.g. 500px x 500px => 500
def PlotGraspFile(filename,datsize):
	#read detector centres from a file of x,y coordinats generated previously
	readd=np.zeros((992,2))
	file=open('ReferenceData/detcentres.txt','r')
	j=0
	for line in file:
	
	     readd[j][0]=line.split()[0]
	     readd[j][1]=line.split()[1]
	     j += 1
	file.close()
	
	
	readv=np.zeros((992,4,2))
	file=open('ReferenceData/vertices.txt','r')
	j=0
	for line in file:
	
	     readv[int(j/4)][j%4][0]=line.split()[0]
	     readv[int(j/4)][j%4][1]=line.split()[1]
	#     print int(j/4), j%4
	     j += 1
	file.close()
	
	
	#plt.figure()
	#vertex = inst.detector.vertex[..., :2]
	#detcenters = inst.detector.center[..., :2]
	#for d in xrange(496,744):
	#    plt.plot(readd[d,0], readd[d,1],'ro')
	#
	#for i in xrange(992): plt.plot(readv[i,:,0], readv[i,:,1], color='blue')
	#plt.show()
	
	#for marcos model 500x500
	#for my models 241x241
	nx=datsize
	ny=datsize
	
	allampX = np.zeros((ny,nx))
	allphiX = np.zeros((ny,nx))
	allampY = np.zeros((ny,nx))
	allphiY = np.zeros((ny,nx))
	TotalI= np.zeros((ny,nx))
	
	allampXre = np.zeros((ny,nx))
	allampXim = np.zeros((ny,nx))
	allampYim = np.zeros((ny,nx))
	allampYre = np.zeros((ny,nx))
	
	file = filename 
	
	data = np.loadtxt(file, skiprows=12)
	allampXre[:,:] = np.reshape(data[:,0],(ny,nx))   # for batch run 2 swap 0,1 2,3
	allampXim[:,:] = np.reshape(data[:,1],(ny,nx))
	allampX[:,:]=np.sqrt(allampXre[:,:]**2+allampXim[:,:]**2)
	allampYre[:,:] = np.reshape(data[:,2],(ny,nx))
	allampYim[:,:] = np.reshape(data[:,3],(ny,nx))
	allampY[:,:]=np.sqrt(allampYre[:,:]**2+allampYim[:,:]**2)
	
	allphiX[:,:]=np.arctan2(allampXim[:,:],allampXre[:,:])
	allphiY[:,:]=np.arctan2(allampYim[:,:],allampYre[:,:])
	
	TotalI[:,:]=allampX[:,:]**2+allampY[:,:]**2
	
	#testing data shpes
	print allampX.shape, allampX[0]
	
	fig = plt.figure()
	
	#plt.subplot(3,2,1)
	#plt.imshow(allampX[:,:],origin="lower")
	ax1 = fig.add_subplot(321)
	im = ax1.imshow(allampX[:,:],origin="lower",extent=[-.051,.051,-.051,.051])
	plt.colorbar(im)
	plt.title('amplitude (x component)', fontsize=10)
	
	#X,Y=np.meshgrid(xx,yy)
	#plt.contour(X,Y,allampX[:,:],levels=levels, colors='black')
	#plt.title(ii)
	#plt.subplot(3,2,2)
	ax2 = fig.add_subplot(322)
	im = ax2.imshow(allphiX[:,:],origin="lower",extent=[-.051,.051,-.051,.051])
	#plt.imshow(allphiX[ii,:,:],vmin=-np.pi,vmax=np.pi, extent = [xmin,xmax, ymin, ymax],origin="lower")
	#plt.imshow(allphiX[:,:], origin="lower")
	plt.colorbar(im)
	plt.title('phase (x component)', fontsize=10)
	
	ax3 = fig.add_subplot(323)
	im = ax3.imshow(allampY[:,:],origin="lower",extent=[-.051,.051,-.051,.051])
	
	#plt.subplot(3,2,3)
	#plt.imshow(allampY[:,:],origin="lower")
	plt.colorbar(im)
	plt.title('amplitude (y component)', fontsize=10)
	#plt.contour(X,Y,allampY[:,:],levels=levels2, colors='white')
	#plt.subplot(3,2,4)
	#plt.imshow(allphiY[:,:],vmin=-np.pi,vmax=np.pi ,origin="lower")
	ax4 = fig.add_subplot(324)
	im = ax4.imshow(allphiY[:,:],vmin=-np.pi,vmax=np.pi ,origin="lower",extent=[-.051,.051,-.051,.051])
	plt.colorbar(im)
	plt.title('phase (y component)', fontsize=10)
	
	#plt.subplot(3,2,5)
	ax5 = fig.add_subplot(325)
	im = ax5.imshow(TotalI[:,:],origin="lower",extent=[-.051,.051,-.051,.051])
	#plt.subplot(3,2,5)
	#plt.imshow(TotalI[:,:],origin="lower")
	plt.colorbar(im)
	plt.title('Intensity (xamp^2 + yamp^2)', fontsize=10)
	#plt.draw()  
	
	
	det_value=np.zeros((992,3)) # 1st will contain total signal, second is number of points, third is average
	
	xx = np.linspace(-.051, .051, 500) # from GRASP file, should probably read this from header
	yy = np.linspace(-.051, .051, 500)
	
	XX, YY = np.meshgrid(xx, yy)  
	
	      
	for i in xrange(nx/2):
	    for j in xrange(ny/2):
	        for d in xrange(496,744):
	            if readv[d,2,0] <= XX[i,j] and XX[i,j] <= readv[d,3,0] and readv[d,2,1] <= YY[i,j] and YY[i,j] <= readv[d,1,1]:
	                det_value[d,0] += TotalI[i,j]
	                det_value[d,1] += 1
	            if det_value[d,1] !=0: # so long as there is some signal on the detector
	                det_value[d,2]=det_value[d,0]/det_value[d,1]  # calc average
	            else:  
	                det_value[d,2]=0   
	            
	
	import matplotlib.colors as colors
	import matplotlib.cm as cmx
	cm = plt.get_cmap('viridis')
	cNorm  = colors.Normalize(vmin=np.amin(TotalI), vmax=np.amax(TotalI))
	scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)
	
	ax6 = fig.add_subplot(326)
	im = ax6.scatter(readd[496:744,0],readd[496:744,1],color=scalarMap.to_rgba(det_value[496:744,2])) 
	#plt.subplot(3,2,6)
	#plt.scatter(readd[496:744,0],readd[496:744,1],color=scalarMap.to_rgba(det_value[496:744,2])) 
	
	scalarMap.set_array(det_value[496:744,2]) # all this to get colourmap
	plt.colorbar(scalarMap)
	plt.xlim(-.051,.051)# cover +/- 60 mm bit bigger than the focal plane
	plt.ylim(-.051,.051)
	plt.title('Intensity (TD pixels)', fontsize=10)
	pos5 = ax5.get_position().bounds
	pos2 = ax2.get_position().bounds
	newpos = [pos2[0]+.05,pos5[1],pos2[2]-.05,pos5[3]]
	ax6.set_position(newpos)
	
	      
	plt.show()
	
	return

