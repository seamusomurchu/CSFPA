# %cd "C:\Users\Creidhe\Documents\OneDrive - Maynooth University\Work\My Research\Graduate Students\James M 2017 -"
import numpy as np
import scipy
import scipy.constants # not automatically imported in line above
import matplotlib.pyplot as plt

#this program assumes that he following files exist in this directory: 
#detcentres.txt
#vertices.txt
#hornfield.grd   (GRASP file from horn)

# GRASP file read in, it would be better to read these from the header
nx = 1001  # number of points specified in GRASP
ny = 1001
DPs = 1001
extent=2*1000  # size of grid side in mm, here -1000 mm to +1000 mm spec. in GRASP
pixelarea = float(extent)/(nx-1)*extent/(nx-1)  # in mm, assume square
freq = 150 # frequency in GHz
wavel = scipy.constants.speed_of_light/(freq*10**9)*1000 # wavelength in mm

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
     j += 1
file.close()


allampX = np.zeros((ny,nx))
allphiX = np.zeros((ny,nx))
allampY = np.zeros((ny,nx))
allphiY = np.zeros((ny,nx))
TotalI= np.zeros((ny,nx))

allampXre = np.zeros((ny,nx))
allampXim = np.zeros((ny,nx))
allampYim = np.zeros((ny,nx))
allampYre = np.zeros((ny,nx))

#file = 'hornfield.grd'  
#file = 'ReferenceData/QBfh12.grd'
file = 'gbmthou.grd'

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

# convvert into watts by xk^2 to find watts/mm and then multiply by pixel area.
totalpower=np.sum(TotalI)*(2*np.pi/wavel)*(2*np.pi/wavel)*pixelarea
print 'total power:',totalpower
print 'total power/pi:',totalpower/np.pi


fig = plt.figure()

ax1 = fig.add_subplot(321)
im = ax1.imshow(allampX[:,:],origin="lower",extent=[-.1,.1,-.1,.1])
plt.colorbar(im)
plt.title('amplitude (x component)', fontsize=10)

ax2 = fig.add_subplot(322)
im = ax2.imshow(allphiX[:,:],origin="lower",extent=[-.1,.1,-.1,.1])
plt.colorbar(im)
plt.title('phase (x component)', fontsize=10)

ax3 = fig.add_subplot(323)
im = ax3.imshow(allampY[:,:],origin="lower",extent=[-.1,.1,-.1,.1])
plt.colorbar(im)
plt.title('amplitude (y component)', fontsize=10)

ax4 = fig.add_subplot(324)
im = ax4.imshow(allphiY[:,:],vmin=-np.pi,vmax=np.pi ,origin="lower",extent=[-.1,.1,-.1,.1])
plt.colorbar(im)
plt.title('phase (y component)', fontsize=10)


ax5 = fig.add_subplot(325)
im = ax5.imshow(TotalI[:,:],origin="lower",extent=[-.1,.1,-.1,.1])
plt.colorbar(im)
plt.title('Intensity (xamp^2 + yamp^2)', fontsize=10)
 


det_value=np.zeros((992,3)) # 1st will contain total signal, second is number of points, third is average

xx = np.linspace(-.1, .1, DPs) # from GRASP file, should probably read this from header
yy = np.linspace(-.1, .1, DPs)

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
