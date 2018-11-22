import qubic
import glob
import numpy as np
import os
import timeit
from CSFPA_dataIO import getXYcoords, dataIO, dataAnalysis, SaveVars, IntensityCalc, IntensityCalcRAW

def MainProg(filename): 
    start = timeit.default_timer()
    
    print filename, "passing filename test"
    #scene = QubicScene(256)
    #inst = instrument.QubicInstrument(filter_nu=150e9)
#    inst = instrument.QubicInstrument()
#    centers = inst.horn.center[:,0:2]
#    detcenters = inst.detector.center[..., :2]
    d = qubic.qubicdict.qubicDict()
    d.read_from_file('/home/james/qubic/qubic/scripts/global_default_FI.dict')

    q = qubic.QubicMultibandInstrument(d)
    
    rep = "/home/james/CF-Source-Focal-Place-Analysis/UItest"
    
    files = glob.glob(rep+filename)
    files.sort()
    
    #vtxs = vertexes of TD detectors
#    vtxs = inst.detector.vertex[496:744]
#    #full detector setup
#    vtxsF = inst.detector.vertex
    
    #SET DETECTOR VERTEXES TO FULL INSTRUMENT
    #q[0].calibration.detarray = '/usr/local/lib/python2.7/dist-packages/qubic/calfiles/CalQubic_DetArray_FI.fits'
    vtxs = q[0].detector.vertex

    #should be 992 for FI
    #vtxcounter = np.zeros(248)
    vtxcounter = np.zeros(992)    
    #DEBUG
    print "vtxs = ", vtxs.shape
    print "vtxcounter = ", vtxcounter.shape

        
    MagXarr, PhaXarr, ReXarr, ImXarr, MagYarr, PhaYarr, ReYarr, ImYarr, vtxcntarr, PixCenX, PixCenY = getXYcoords(filename,vtxs) 

    vtxcounter = np.vstack((vtxcounter,vtxcntarr))
    vtxcounter = vtxcounter.T
    vtxcounter = vtxcounter[:,1:3]
        
    #IntX = (ReXarr*ReXarr) + (ImXarr*ImXarr)
    #IntY = (ReYarr*ReYarr) + (ImYarr*ImYarr)
    #IntT = IntX[:] + IntY[:]
	
	#outsourcing intensity calc to dataIO
    IntX, IntY, IntT = IntensityCalc(MagXarr, PhaXarr, MagYarr, PhaYarr)  
    print "intensity tests", IntX.shape   
    #use this order for a header
    #dat = np.hstack((MagXmat,vtxcounter,ReXmat,ImXmat,ReYmat,ImYmat))
    dat = np.vstack((MagXarr, PhaXarr, ReXarr, ImXarr, MagYarr, PhaYarr, ReYarr, ImYarr, vtxcntarr, PixCenX, PixCenY, IntX, IntY, IntT))
    dat = dat.T
    #SAVE DATA TO MAKE LOADING EASY
    #create strings for saving to file IO
    datstring = "dat"
    dataIO(dat,datstring)
    
    datmodstring = "datmod"
    datmod = dataAnalysis(dat) # THIS DIVIDES BY NUMBER OF POINTS PER PIXEL
    dataIO(datmod,datmodstring)
    
    #load data for plotting raw modal data
    dataCF1 = np.loadtxt(filename, skiprows=1) 
    xycoords = np.array(dataCF1[:,2:4])
    
    #plotting RAW INTENSITY
    #Ix = (dataCF1[:,4]*np.cos(dataCF1[:,5]))**2 + (dataCF1[:,4]*np.sin(dataCF1[:,5]))**2
    #Iy = (dataCF1[:,6]*np.cos(dataCF1[:,7]))**2 + (dataCF1[:,6]*np.sin(dataCF1[:,7]))**2
    #IT = Ix + Iy
	
    Ix, Iy, IT = IntensityCalcRAW(filename)
	
    #testing setting zeros to NANs
    ITnans = [np.nan if x == 0 else x for x in IT]
    ITnans = np.asarray(ITnans)
    
    #save vars as local 
    SaveVars(MagXarr, PhaXarr, ReXarr, ImXarr, MagYarr, PhaYarr, ReYarr, ImYarr, vtxcntarr, PixCenX, PixCenY, IntX, IntY, IntT, Ix, Iy, IT, xycoords, filename)    
    
    os.system('spd-say "Main program has finished"')
    stop = timeit.default_timer()
    time = stop - start
    seconds = (time - int(time)) * 60
    print time/60, "m", seconds, "s"
    
    return