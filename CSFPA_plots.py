import matplotlib.pyplot as plt
import numpy as np
import os
from CSFPA_dataIO import RetrieveVars
import pickle #ignore warning, seems like RetrieveVars uses it


#def TotalIntensityPlot(PixCenX,PixCenY,IntT,xycoords,IT):
def TotalIntensityPlot():
    MagXarr, PhaXarr, ReXarr, ImXarr, MagYarr, PhaYarr, ReYarr, ImYarr, vtxcntarr, PixCenX, PixCenY, IntX, IntY, IntT, Ix, Iy, IT, xycoords, filename = RetrieveVars()
    ######################Total Intensity plot - Normalised
    
    plt.figure()
    plt.subplot(121)
    plt.scatter(PixCenX*1000,PixCenY*1000, c=IntT[:]/max(IntT[:]), cmap='plasma',marker='s')
    plt.axis([-60, 60, -60, 60])
    plt.axis('equal')
    plt.title("CF1 Source as Bolometers Total Instensity",fontsize=10)
    plt.subplot(122)
    plt.scatter(xycoords[:,0],xycoords[:,1], c=IT[:]/max(IT[:]), cmap='plasma',marker='.')
    plt.axis([-60, 60, -60, 60])
    plt.axis('equal')
    plt.title("CF1 Source - MODAL",fontsize=10)
    plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
    cax = plt.axes([0.85, 0.1, 0.05, 0.8])
    plt.colorbar(cax=cax,label="Intensity")
    plt.show()
    os.system('spd-say "BING! BING! BING!"')
    return

def IntensityXPlot():
    ######################IntensityX plot
    MagXarr, PhaXarr, ReXarr, ImXarr, MagYarr, PhaYarr, ReYarr, ImYarr, vtxcntarr, PixCenX, PixCenY, IntX, IntY, IntT, Ix, Iy, IT, xycoords, filename = RetrieveVars()
    
    plt.figure()
    plt.subplot(121)
    plt.scatter(PixCenX*1000,PixCenY*1000, c=IntX/max(IntX), s=8, cmap='plasma',marker='s') 
    plt.axis([-0.06, 0.06, -0.06, 0.06])
    plt.axis('equal')   
    plt.title("CF1 Source as Bolometers Intensity X dir",fontsize=10)
    plt.subplot(122)
    plt.scatter(xycoords[:,0],xycoords[:,1], c=Ix/max(Ix), cmap='plasma',marker='.')
    plt.axis([-0.06, 0.06, -0.06, 0.06])
    plt.axis('equal')    
    plt.title("CF1 Source - MODAL",fontsize=10)    
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

def MagXPlot():
    #load saved variables
    MagXarr, PhaXarr, ReXarr, ImXarr, MagYarr, PhaYarr, ReYarr, ImYarr, vtxcntarr, PixCenX, PixCenY, IntX, IntY, IntT, Ix, Iy, IT, xycoords, filename = RetrieveVars()
    #load raw data from file
    dataCF = np.loadtxt(filename, skiprows=1) 
    plt.figure()
    plt.subplot(121)
    plt.scatter(PixCenX*1000,PixCenY*1000, c=MagXarr/max(MagXarr), s=8, cmap='plasma',marker='s')   
    plt.axis([-0.06, 0.06, -0.06, 0.06])
    plt.axis('equal')    
    plt.title("Source as Bolometers",fontsize=10)
    plt.subplot(122)
    plt.scatter(xycoords[:,0],xycoords[:,1], c=dataCF[:,4]/(max(dataCF[:,4])), cmap='plasma',marker='.')
    plt.axis([-0.06, 0.06, -0.06, 0.06])
    plt.axis('equal')    
    plt.title("Source - MODAL",fontsize=10)    
    plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
    cax = plt.axes([0.85, 0.1, 0.05, 0.8])
    plt.colorbar(cax=cax,label="Mag X")    
    plt.show()
    
    return

def MagYPlot():
    MagXarr, PhaXarr, ReXarr, ImXarr, MagYarr, PhaYarr, ReYarr, ImYarr, vtxcntarr, PixCenX, PixCenY, IntX, IntY, IntT, Ix, Iy, IT, xycoords, filename = RetrieveVars()
    #load raw data from file
    dataCF = np.loadtxt(filename, skiprows=1) 
    ############################### plot normalised data ################
    plt.figure()
    plt.subplot(121)
    plt.scatter(PixCenX*1000,PixCenY*1000, c=MagYarr/max(MagYarr), s=8, cmap='plasma',marker='s')  
    plt.axis([-0.06, 0.06, -0.06, 0.06])
    plt.axis('equal')    
    plt.title("Mag Y CF Source as Bolometers",fontsize=10)
    plt.subplot(122)
    plt.scatter(xycoords[:,0],xycoords[:,1], c=dataCF[:,6]/(max(dataCF[:,6])), cmap='plasma',marker='.')
    plt.axis([-0.06, 0.06, -0.06, 0.06])
    plt.axis('equal')    
    plt.title("Mag Y CF Source - MODAL",fontsize=10)    
    plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
    cax = plt.axes([0.85, 0.1, 0.05, 0.8])
    plt.colorbar(cax=cax,label="Mag Y")    
    plt.show()
    
    return

def PhaXPlot():
    #Double check this result. Looks quite odd pattern on TESs
    MagXarr, PhaXarr, ReXarr, ImXarr, MagYarr, PhaYarr, ReYarr, ImYarr, vtxcntarr, PixCenX, PixCenY, IntX, IntY, IntT, Ix, Iy, IT, xycoords, filename = RetrieveVars()
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