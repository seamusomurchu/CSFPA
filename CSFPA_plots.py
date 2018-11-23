import matplotlib.pyplot as plt
import numpy as np
import os
from CSFPA_dataIO import RetrieveVars
import pickle #ignore warning, seems like RetrieveVars uses it


#def TotalIntensityPlot(PixCenX,PixCenY,IntT,xycoords,IT):
def TotalIntensityPlot(plotfname):
    MagXarr, PhaXarr, ReXarr, ImXarr, MagYarr, PhaYarr, ReYarr, ImYarr, vtxcntarr, PixCenX, PixCenY, IntX, IntY, IntT, Ix, Iy, IT, xycoords, filename = RetrieveVars(plotfname)
    ######################Total Intensity plot - Normalised
    
    plt.figure(facecolor='xkcd:pale green')
    plt.subplot(121, facecolor='#d8dcd6')
    plt.scatter(PixCenX*1000,PixCenY*1000, c=IntT[:]/max(IntT[:]), cmap='jet',marker='s')
    plt.axis([-60, 60, -60, 60])
    plt.axis('equal')
    plt.title("{} Bolometers Total Instensity".format(plotfname),fontsize=10)
    plt.subplot(122, facecolor='#d8dcd6')
    plt.scatter(xycoords[:,0],xycoords[:,1], c=IT[:]/max(IT[:]), cmap='jet',marker='.')
    plt.axis([-60, 60, -60, 60])
    plt.axis('equal')
    plt.title("RAW - {}".format(filename),fontsize=10)
    plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
    cax = plt.axes([0.85, 0.1, 0.05, 0.8])
    plt.colorbar(cax=cax,label="Intensity")
    plt.show()
    os.system('spd-say "BING! BING! BING!"')
    return

def IntensityXPlot(plotfname):
    ######################IntensityX plot
    MagXarr, PhaXarr, ReXarr, ImXarr, MagYarr, PhaYarr, ReYarr, ImYarr, vtxcntarr, PixCenX, PixCenY, IntX, IntY, IntT, Ix, Iy, IT, xycoords, filename = RetrieveVars(plotfname)
    
    plt.figure(facecolor='xkcd:pale green')
    plt.subplot(121, facecolor='#d8dcd6')#xkcd reference for this colour
    plt.scatter(PixCenX,PixCenY, c=IntX/max(IntX), s=25, cmap='jet',marker='s') 
    plt.axis([-0.06, 0.06, -0.06, 0.06])
    plt.axis('equal')   
    plt.title("{} as Bolometers Intensity X dir".format(plotfname),fontsize=10)
	
    plt.subplot(122, facecolor='#d8dcd6')#xkcd reference for this colour
    plt.scatter(xycoords[:,0],xycoords[:,1], c=Ix/max(Ix), cmap='jet',marker='.')
    plt.axis([-0.06, 0.06, -0.06, 0.06])
    plt.axis('equal')    
    plt.title("{}".format(plotfname),fontsize=10)    
    plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
    cax = plt.axes([0.85, 0.1, 0.05, 0.8])
    plt.colorbar(cax=cax,label="Intensity X")    
    plt.show()
    
    return

def IntensityYPlot():
    MagXarr, PhaXarr, ReXarr, ImXarr, MagYarr, PhaYarr, ReYarr, ImYarr, vtxcntarr, PixCenX, PixCenY, IntX, IntY, IntT, Ix, Iy, IT, xycoords, filename = RetrieveVars()
    ######################Intensity Y plot
    plt.figure()
    plt.subplot(121)
    plt.scatter(PixCenX*1000,PixCenY*1000, c=IntY/max(IntY), s=8, cmap='plasma',marker='s')
    plt.axis([-0.06, 0.06, -0.06, 0.06])
    plt.axis('equal')   
    plt.title("CF1 Source as Bolometers Intensity Y dir",fontsize=10)
    plt.subplot(122)
    plt.scatter(xycoords[:,0],xycoords[:,1], c=Iy/max(Iy), cmap='plasma',marker='.')
    plt.axis([-0.06, 0.06, -0.06, 0.06])
    plt.axis('equal')    
    plt.title("CF1 Source - MODAL",fontsize=10)    
    plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
    cax = plt.axes([0.85, 0.1, 0.05, 0.8])
    plt.colorbar(cax=cax,label="Intensity Y")    
    plt.show()
    
    return

def MagXPlot(plotfname):
    #load saved variables
    MagXarr, PhaXarr, ReXarr, ImXarr, MagYarr, PhaYarr, ReYarr, ImYarr, vtxcntarr, PixCenX, PixCenY, IntX, IntY, IntT, Ix, Iy, IT, xycoords, filename = RetrieveVars(plotfname)
    #load raw data from file
    dataCF = np.loadtxt(filename, skiprows=1) 
    plt.figure(facecolor='xkcd:pale green')
    plt.subplot(121, facecolor='#d8dcd6')
    plt.scatter(PixCenX,PixCenY, c=MagXarr/max(MagXarr), s=25, cmap='jet',marker='s')   
    plt.axis([-0.055, 0.055, -0.055, 0.055])
    plt.axis('equal')    
    plt.title("{} as Bolometers".format(plotfname),fontsize=10)
    #plt.plot(0, 0, 'o', mfc='none',markersize=57.16*2,color='black')
    plt.subplot(122, facecolor='#d8dcd6')
    plt.scatter(xycoords[:,0],xycoords[:,1], c=dataCF[:,4]/(max(dataCF[:,4])), cmap='jet',marker='.')
    #plt.scatter(xycoords[:,0],xycoords[:,1], c=MagXarr/(max(MagXarr)), cmap='plasma',marker='.')
    #plt.plot(0, 0, 'o', mfc='none',markersize=57.16*2,color='black')
    plt.axis([-0.055, 0.055, -0.055, 0.055])
    plt.axis('equal')    
    plt.title("Source - {}".format(filename),fontsize=10)    
    plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
    cax = plt.axes([0.85, 0.1, 0.05, 0.8])
    plt.colorbar(cax=cax,label="Mag X")    
    plt.show()
    
    return

def MagYPlot(plotfname, filename):
    MagXarr, PhaXarr, ReXarr, ImXarr, MagYarr, PhaYarr, ReYarr, ImYarr, vtxcntarr, PixCenX, PixCenY, IntX, IntY, IntT, Ix, Iy, IT, xycoords, filename = RetrieveVars(plotfname)
    #load raw data from file
    dataCF = np.loadtxt(filename, skiprows=1) 
    ############################### plot normalised data ################
    plt.figure()
    plt.subplot(121)
    plt.scatter(PixCenX*1000,PixCenY*1000, c=MagYarr/max(MagYarr), s=8, cmap='jet',marker='s')  
    plt.axis([-0.06, 0.06, -0.06, 0.06])
    plt.axis('equal')    
    plt.title("Mag Y {} as Bolometers".format(filename),fontsize=10)
    plt.subplot(122)
    plt.scatter(xycoords[:,0],xycoords[:,1], c=dataCF[:,6]/(max(dataCF[:,6])), cmap='jet',marker='.')
    plt.axis([-0.06, 0.06, -0.06, 0.06])
    plt.axis('equal')    
    plt.title("Mag Y {}".format(filename),fontsize=10)    
    plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
    cax = plt.axes([0.85, 0.1, 0.05, 0.8])
    plt.colorbar(cax=cax,label="Mag Y")    
    plt.show()
    
    return

def PhaXPlot(plotfname):
    #Double check this result. Looks quite odd pattern on TESs
    MagXarr, PhaXarr, ReXarr, ImXarr, MagYarr, PhaYarr, ReYarr, ImYarr, vtxcntarr, PixCenX, PixCenY, IntX, IntY, IntT, Ix, Iy, IT, xycoords, filename = RetrieveVars(plotfname)
    #load raw data from file
    dataCF = np.loadtxt(filename, skiprows=1) 
    ############################### plot normalised data ################
    plt.figure()
    plt.subplot(121)
    plt.scatter(PixCenX*1000,PixCenY*1000, c=PhaXarr/max(PhaXarr), s=8, cmap='plasma',marker='s')  
    plt.axis([-0.06, 0.06, -0.06, 0.06])
    plt.axis('equal')    
    plt.title("Phase X CF Source as Bolometers",fontsize=10)
    plt.subplot(122)
    plt.scatter(xycoords[:,0],xycoords[:,1], c=dataCF[:,5]/(max(dataCF[:,5])), cmap='plasma',marker='.')
    plt.axis([-0.06, 0.06, -0.06, 0.06])
    plt.axis('equal')    
    plt.title("Phase X CF Source - MODAL",fontsize=10)    
    plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
    cax = plt.axes([0.85, 0.1, 0.05, 0.8])
    plt.colorbar(cax=cax,label="Phase X")    
    plt.show()
    
    return

def PhaYPlot():
    MagXarr, PhaXarr, ReXarr, ImXarr, MagYarr, PhaYarr, ReYarr, ImYarr, vtxcntarr, PixCenX, PixCenY, IntX, IntY, IntT, Ix, Iy, IT, xycoords, filename = RetrieveVars()
    #load raw data from file
    dataCF = np.loadtxt(filename, skiprows=1) 
    ############################### plot normalised data ################
    plt.figure()
    plt.subplot(121)
    plt.scatter(PixCenX*1000,PixCenY*1000, c=PhaYarr/max(PhaYarr), cmap='plasma',marker='s')  
    plt.axis([-0.06, 0.06, -0.06, 0.06])
    plt.axis('equal')    
    plt.title("Phase Y CF Source as Bolometers",fontsize=10)
    plt.subplot(122)
    plt.scatter(xycoords[:,0],xycoords[:,1], c=dataCF[:,7]/(max(dataCF[:,7])), cmap='plasma',marker='.')
    plt.axis([-0.06, 0.06, -0.06, 0.06])
    plt.axis('equal')    
    plt.title("Phase Y CF Source - MODAL",fontsize=10)    
    plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
    cax = plt.axes([0.85, 0.1, 0.05, 0.8])
    plt.colorbar(cax=cax,label="Phase Y")    
    plt.show()
    
    return

def FPComparisonPlot(pkl1,pkl2):
	#initially going to hardcode for intensity or magnitude
	MagXarr, PhaXarr, ReXarr, ImXarr, MagYarr, PhaYarr, ReYarr, ImYarr, vtxcntarr, PixCenX, PixCenY, IntX, IntY, IntT, Ix, Iy, IT, xycoords, filename = RetrieveVars(pkl1)
	IntX1 = IntX/max(IntX)

	plt.figure(facecolor='xkcd:pale green')
	plt.subplot(221, facecolor='#d8dcd6')
	plt.scatter(PixCenX*1000,PixCenY*1000, c=IntX1, cmap='jet',marker='s')
	plt.axis([-60, 60, -60, 60])
	plt.axis('equal')
	plt.title("FP - {}".format(pkl1),fontsize=10)
	
	plt.subplot(222, facecolor='#d8dcd6')
	MagXarr, PhaXarr, ReXarr, ImXarr, MagYarr, PhaYarr, ReYarr, ImYarr, vtxcntarr, PixCenX, PixCenY, IntX, IntY, IntT, Ix, Iy, IT, xycoords, filename = RetrieveVars(pkl2)
	IntX2 = IntX/max(IntX)
	plt.scatter(PixCenX*1000,PixCenY*1000, c=IntX2, cmap='jet',marker='s')
	plt.axis([-60, 60, -60, 60])
	plt.axis('equal')
	plt.title("FP - {}".format(pkl2),fontsize=10)
	
	plt.subplot(223, facecolor='#d8dcd6')
	comp = IntX1 - IntX2
	
	#okay so here i am finding all of the outer pixels and setting to zero
	#this allows me to analyse valid pixels between grasp and modal
	#maybe i should delete these elements of the array to make data analysis easier
	for i in range(len(PixCenX)):
		if np.sqrt(PixCenX[i]**2 + PixCenY[i]**2) > 0.05:	
			comp[i] = 0
			PixCenX[i] = 0.05
			PixCenY[i] = 0.05
			#print "radius test", np.sqrt(PixCenX[i]**2 + PixCenY[i]**2)
			#plt.scatter(PixCenX[i]*1000,PixCenY[i]*1000, c=comp[i], cmap='jet',marker='s')

	plt.scatter(PixCenX*1000,PixCenY*1000, c=comp, cmap='jet',marker='s')
	plt.axis([-60, 60, -60, 60])
	plt.axis('equal')
	plt.title("Data Comparison",fontsize=10)	
	
	plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
	cax = plt.axes([0.85, 0.1, 0.05, 0.8])
	plt.colorbar(cax=cax,label="Comparison")    
	plt.show()	
	
	return

def FPComparisonPlotRAW(pkl1,pkl2):
	#initially going to hardcode for intensity or magnitude
	MagXarr, PhaXarr, ReXarr, ImXarr, MagYarr, PhaYarr, ReYarr, ImYarr, vtxcntarr, PixCenX, PixCenY, IntX, IntY, IntT, Ix, Iy, IT, xycoords, filename = RetrieveVars(pkl1)
	IntX1 = Ix/max(Ix)

	plt.figure()
	plt.subplot(221)
	plt.scatter(xycoords[:,0],xycoords[:,1], c=IntX1, cmap='jet',marker='s')
	plt.axis([-60, 60, -60, 60])
	plt.axis('equal')
	plt.title("pkl1",fontsize=10)
	
	plt.subplot(222)
	MagXarr, PhaXarr, ReXarr, ImXarr, MagYarr, PhaYarr, ReYarr, ImYarr, vtxcntarr, PixCenX, PixCenY, IntX, IntY, IntT, Ix, Iy, IT, xycoords, filename = RetrieveVars(pkl2)
	IntX2 = Ix/max(Ix)
	plt.scatter(xycoords[:,0],xycoords[:,1], c=IntX2, cmap='jet',marker='s')
	plt.axis([-60, 60, -60, 60])
	plt.axis('equal')
	plt.title("pkl2",fontsize=10)
	
	plt.subplot(223)
	comp = IntX1 - IntX2
	plt.scatter(xycoords[:,0],xycoords[:,1], c=comp, cmap='jet',marker='s')			
	plt.axis([-60, 60, -60, 60])
	plt.axis('equal')
	plt.title("Data Comparison",fontsize=10)	
	
	plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
	cax = plt.axes([0.85, 0.1, 0.05, 0.8])
	plt.colorbar(cax=cax,label="Comparison")    
	plt.show()	
	
	return