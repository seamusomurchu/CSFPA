#! /usr/bin/python2.7
import numpy as np
import pandas as pd
import glob
import re
import os
from operator import itemgetter
import csv

"""Program for formating grasp and/or modal files
grasp header explained = https://ftp.space.dtu.dk/pub/ticra

Current version is 'functional'. Still need to implement;
MODAL header method
User defined directories/reps
"""

#user defined directories for input/output locations
#look up implementing dialogue for this
#print "Remember to select your input and output directories"
#graspinputrep  = "/home/james/GraspModalDataIO/qbdataio/"
#graspoutputrep = "/home/james/GraspModalDataIO/qbdataio/iodata/"
#modalinputrep  = "/home/jmurphy/qbdataio_data/modal_nhorns/"
#modaloutputrep = "/home/jmurphy/qbdataio_data/modal_nhorns/iodata/"

#Horn numbering refence file
#hornref = "/home/james/GraspModalDataIO/qbdataio/CalQubic_HornArray_v3.txt"
#put in functions for matrixes,calculations,amplitude, phase etc here
#do source field name
#function if grasp file
def getgraspinfo(fname):

	#find horn num from input file THIS DEPENDS ON WHETHER THE INPUT FILES ARE NAMED CORRECTLY
	fname2 = re.findall('([^/]+$)', fname)
	fname2 = re.findall(r'\d+', str(fname2))
	print "fname2  info = ", fname2, len(fname2), type(fname2)
	#horn_conv = str(fname2[0])
	#print "horn_conv", horn_conv, type(horn_conv)

	#get horn id row/col

	#horn_num = getgrasphorn(fname)
	#print "horn_num", horn_num

	#Check if grasp file has right naming convention
#	if len(fname2) == 4:	
#		horn_num = getgrasphorn(fname)
#		horn_bool = "Horn numbering nomenclature (appears) correct based of input data."
#	else:
#		horn_num = main_index
#		horn_bool = "Horn numbering nomenclature is not representative"

	#open file and read header information
	infile = open(fname,'r')

	freqindex = 20
	iktype = 20
	iparams = 20
	ixiy_index = 20
	GRASPgridarea = 20
	GRASPpixels = 20
	datastart = 20
	for i in range(20):
		temp = infile.readline()
		print i, temp

		if 'FREQUENCIES [GHz]:' in temp:
			freqindex = i + 1
			print freqindex

		if i == freqindex:
			frequency = temp
			#print frequency

		if '++++' in temp:			#this line catches the end of header by finding '++++'
			print 'found +++', i
			headerend = i
			iktype = i + 1
			iparams = i + 2
			ixiy_index = i + 3
			GRASPgridarea = i + 4
			GRASPpixels = i + 5
			datastart = i + 6

		#some of these will require operations
		if i == iktype:
			ktype = temp
		if i == iparams:
			param = temp	
			params = [float(s) for s in param.split()]
			params = np.asarray(params)
		if i == ixiy_index:
			ixiy = temp
			ixiyparam = [float(s) for s in ixiy.split()]
			ixiyparam = np.asarray(ixiyparam)
			
		if i == GRASPgridarea:		#sets grid area into array
			gridarea = temp 
			print gridarea                
			dims = [float(s) for s in gridarea.split()]
			dims = np.asarray(dims)
			print dims[0],dims[2]
		if i == GRASPpixels:
			gpix = temp
			pdims = [float(s) for s in gpix.split()]
			pdims = np.asarray(pdims)

		#i = 16

	return frequency, dims, pdims, ktype, params, ixiyparam, datastart

#function returns horn naming info e.g. ID, row, col OR bad input filename
#it works like a lookup table referencing hdata
def getgrasphorn(fname):

	fname2 = re.findall('([^/]+$)', fname)
	fname2 = re.findall(r'\d+', str(fname2))
	fname2 = np.asarray(fname2)
	#print "fname2 ", fname2, type(fname2), fname2.shape
	#print "hdata test ", hdata[0,:], hdata.shape[0]

	for i in range(hdata.shape[0]):
		if int(hdata[i,0]) == int(fname2[0]):
			horn_name = hdata[i].astype(int)

	return horn_name

#first 8 params here don't really make logical sense to be here. Could be in getgraspinfo function or a separate one entirely

def gdataform(dims, pdims, datastart, fname):
	#number of 'pixel' points from datafile
	nx = pdims[0]	
	ny = pdims[1]

	xmin = dims[0]
	xmax = dims[2]
	ymin = dims[1]
	ymax = dims[3]

	xx = np.linspace(xmin,xmax,nx)
	yy = np.linspace(ymin,ymax,ny) 

	#could optimise this by just adding xx and yy to all_data
	xy = ([])
	for i in yy:
		for j in xx:
			ji = j,i
			#xy = np.append(xy,ij,axis=0)
			xy.append(ji)

	xya = np.asarray(xy)
	print "xya = ", xya	
	#print len(xy)
	#print xy[0]
	print xya.shape
	#print xya[1,]		
	
	datalen = len(xx)*len(yy)
	zarr = np.zeros(int(datalen))
	zarr = np.asarray(zarr)
	
	print "datastart", datastart, "fname, ", fname
	data = np.loadtxt(fname, skiprows=datastart, delimiter='\t') #choose value dynamically... need to reshape this first, its ruining comb currently

	#this puts data from file into array. could be optimsed by reading straight from file (data)
	data_array = ([])

	for i in data:
		data_array.append(i) 
	data_array = np.asarray(data_array)

	print "data_array "
	print data_array[0,0:2]
	print data_array.shape
	#print datalen

	#do calculations for amp and phase
	ampX = ([])
	phaX = ([])
	ampY = ([])
	phaY = ([])
	ampZ = ([])
	phaZ = ([])
	
	print "len data array", len(data_array)

	for i in range(len(data_array)): #maybe undo, was datalen
		
		ampXvar = np.sqrt(data_array[i,0]**2 + data_array[i,1]**2) 
		ampX.append(ampXvar)

		phaXvar = np.arctan2(data_array[i,1],data_array[i,0])
		phaX.append(phaXvar)

		ampYvar = np.sqrt(data_array[i,2]**2 + data_array[i,3]**2) 
		ampY.append(ampYvar)

		phaYvar = np.arctan2(data_array[i,3],data_array[i,2])
		phaY.append(phaYvar)
		
		ampZvar = np.sqrt(data_array[i,4]**2 + data_array[i,5]**2) 
		ampZ.append(ampZvar)

		phaZvar = np.arctan2(data_array[i,5],data_array[i,4])
		phaZ.append(phaZvar)

	#this could be optimised by leaving as a list before creating data array
	ampX = np.asarray(ampX)	
	phaX = np.asarray(phaX)
	ampY = np.asarray(ampY)
	phaY = np.asarray(phaY)
	ampZ = np.asarray(ampZ)
	phaZ = np.asarray(phaZ)

	#Put individual arrays into one large array
	all_data = np.array([ampX,phaX,ampY,phaY,ampZ,phaZ])

	#transpose array
	all_data = all_data.T
	
	print "all_data shape", all_data.shape
	print "xya shape", xya.shape
	print "zarr", zarr.shape
	
	#reformat xya to include zero arrays to match MODAL style
	#xya = np.vstack((zarr,xya))
	zarrs = np.asarray((zarr,zarr)).T

	#horizontally stack xy location array with data array
	comb_data = np.hstack((xya,all_data))
	comb_data = np.hstack((zarrs,comb_data))
	
	#print "all_data = ", all_data, all_data.shape
	print "comb data = ", comb_data, comb_data.shape
	#print "Xamp"
	#print ampX, ampX.shape, type(ampX)

	#print "phaX"
	#print phaX, phaX.shape

	#print "ampY"
	#print ampY, ampY.shape

	#print "phaY"
	#print phaY, phaY.shape
	
	#print "ampZ"
	#print ampZ, ampZ.shape

	#print "phaZ"
	#print phaZ, phaZ.shape
	
	#pause development here and work on grid area output
	return nx, ny, xmin, xmax, ymin, ymax, comb_data

def writegraspdata(graspoutputrep, fname, freq, nx, ny, xmin, xmax, ymin, ymax, comb_data, horn_bool):

	#write header
	#when opening this file, make it dynamic to write a file for each data file
	f = open(graspoutputrep + 'qboutput_CF'+'CF1test'+'.qb', 'w+')
	f.write('qbdataio GRASP MODAL data' + '\n')
	f.write('This qbdataio output is generated from this grasp file -> ' + str(fname) + '\n')
	f.write(horn_bool + '\n')
	f.write('Simulation Frequency GHz: ' + freq + '\n') #e.g. take GHz dynamicall from grasp file
	f.write('Number of X and Y positions: ' + str(nx) + ' ' + str(ny) + '\n')
	f.write('Geometry Frame: ' + str(xmin) + ' ' + str(ymin) + ' ' + str(xmax) + ' ' + str(ymax) + '\n')
	f.write('***HeaderEnd***' + '\n')
	f.write('Xind               Yind               Ypos               Xpos               Xamp              Xpha              Yamp              Ypha              Zamp              Zpha' + '\n')

	#write combined data array below header
	np.savetxt(f, comb_data, delimiter=' ',fmt='%17.9e %17.9e %17.9e %17.9e %17.9e %17.9e %17.9e %17.9e %17.9e %17.9e')

	f.close
	print "Writing ", graspoutputrep + 'qboutput_CF'+'.qb'

	return 

#try write data with pandas
def PandaGraspWrite(comb_data, graspoutputrep, fname):
	#test comb_data shape
	#setup dict
	comb_dict = {
		'Xind': comb_data[:,0],
		'Yind': comb_data[:,1],
		'Ypos': comb_data[:,2],
		'Xpos': comb_data[:,3],
		'Xamp': comb_data[:,4],
		'Xpha': comb_data[:,5],
		'Yamp': comb_data[:,6],
		'Ypha': comb_data[:,7],
		'Zamp': comb_data[:,8],
		'Zpha': comb_data[:,9]
	}
	
	#create dataframe
	#NB have to swap Xpos & Ypos columns to match MODAL format
	df = pd.DataFrame(comb_dict, columns=['Xind', 'Yind', 'Ypos', 'Xpos', 'Xamp', 'Xpha', 'Yamp', 'Ypha', 'Zamp', 'Zpha'])
	print df
	df.to_csv(graspoutputrep+fname+'_Mstyle.qb', sep='\t', index=False, float_format='%.9e')
	return

#this is setup for when modal header is properly inplemented
def getmodalinfo(fname, main_index):

	#open modal file to pull header info
	horn_conv = re.findall(r'\d+', fname)
	#horn_conv = str(horn_conv[1])
	print "horn_conv", horn_conv, type(horn_conv), len(horn_conv)

	#if condition checks if modal filename has correct form for naming convention
	if len(horn_conv) == 2:
		horn_name = getmodalhorn(fname)
		horn_bool = "Horn numbering nomenclature (appears) correct based of input data."
		#print "match, horn name = ", horn_name
	else:
		horn_name = (main_index, "na", "na")
		horn_bool = "Horn numbering nomenclature is not representative"

	return horn_name, horn_bool

#this function works like a lookup table for converting modal rows&columns to horn num cvonvention
def getmodalhorn(fname):

	fname2 = re.findall('([^/]+$)', fname)
	fname2 = re.findall(r'\d+', str(fname2))
	fname2 = np.asarray(fname2)
	#print "horn_conv", fname2, type(fname2)
	
	#print "hdata", hdata, hdata.shape[0], type(hdata)

	#print hdata[0,0]
	
	#so in here im trying to match values from modal filename with a lookup array horn nums
	#hdata has form [horn ID, row, col] == [horn ID, xpos, ypos] given by CalQubic_HornArray_v3.txt (ATRIUM)
	for i in range(hdata.shape[0]):
		#print hdata[i,0], "hdata", int(hdata[i,1]), hdata[i,2], i, "fname", fname2[0], fname2[1] 

		#need to double check rows and cols with dave
		if int(fname2[0]) == int(hdata[i,1]) and int(fname2[1]) == int(hdata[i,2]):
			
			horn_name = hdata[i].astype(int)
			#print "match, horn name = ", horn_name
	
	return horn_name
	
def mdataform(fname):
	#print fname
	data = np.loadtxt(fname, skiprows=1) #fix skip rows to be dynamic
	data = np.array(data[:,2:10])
	
	#print "data print test", data, data.shape
	return data

def writemodaldata(modaloutputrep, comb_data, fname, horn_name, horn_bool):
	
	#write header
	#when opening this file, make it dynamic to write a file for each data file
	f = open(modaloutputrep + 'qboutput_hornid'+str(horn_name[0])+'_row'+str(horn_name[1])+'_col'+str(horn_name[2])+'.qb', 'w+')
	f.write('qbdataio GRASP MODAL data' + '\n')
	f.write('This qbdataio output is generated from this grasp file -> ' + str(fname) + '\n')
	f.write(horn_bool + '\n')
	#f.write('Simulation Frequency GHz: ' + freq + '\n') #e.g. take GHz dynamicall from grasp file
	#f.write('Number of X and Y positions: ' + str(nx) + ' ' + str(ny) + '\n')
	#f.write('Geometry Frame: ' + str(xmin) + ' ' + str(ymin) + ' ' + str(xmax) + ' ' + str(ymax) + '\n')
	f.write('***HeaderEnd***' + '\n')
	f.write('Ypos               Xpos               Xamp              Xpha              Yamp              Ypha              Zamp              Zpha' + '\n')

	#write combined data array below header
	np.savetxt(f, comb_data, delimiter=' ',fmt='%17.9e %17.9e %17.9e %17.9e %17.9e %17.9e %17.9e %17.9e ')

	f.close

	return 

def DataIOMain(filename):
	# output location, use second for multi frequency analysis
	graspoutputrep = "/home/james/files4CSFPA/Fromqbdataio/"
	#get info from grasp file
	freq, dims, pdims, ktype, params, ixiyparam, datastart = getgraspinfo(filename)
	#get info from those returned paramters ###I'm sure I had a reason for this
	nx, ny, xmin, xmax, ymin, ymax, comb_data = gdataform(dims, pdims, datastart, filename)
	#modify filename for saving - can probably simplify and delete these lines
	fname2 = os.path.basename(filename)
	fname2 = os.path.splitext(fname2)[0]
	#write data with filename
	PandaGraspWrite(comb_data, graspoutputrep, fname2)
	
	return

#"""Start of Main"""
#
##user defines whether grasp or modal files for conversion
##could actually just write 2 separate programs
#mode = raw_input("Please select file type for conversion (GRASP/MODAL): ")
#print mode
#
##load horn ref matrix
#hdata = np.loadtxt(hornref,skiprows=15)
#hdata = hdata[:,0:3]
##print hdata
##Check file type. Grasp or modal
##calls function for program type e.g. grasp or modal
#if ('g' in mode) or ('G' in mode):
#
#	#rep = "/home/jmurphy/qbdataio/graspdata/"
#	files = sorted(glob.glob(graspinputrep+'*.grd'))
#	main_index = 0
#	
#	for fname in files:
#
#		#print fname
#		#print "horn_num = ", horn_num
#
#		freq, dims, pdims, ktype, params, ixiyparam, horn_num, horn_bool, datastart = getgraspinfo(fname, main_index)
#		#technically this function could exist before the loop
#		#print freq, dims, pdims, ktype, params, ixiyparam
#	
#		nx, ny, xmin, xmax, ymin, ymax, comb_data = gdataform(dims, pdims, datastart)
#		#print "comb_data from function = ", comb_data
#
#		#function output to file
#		#writegraspdata(graspoutputrep, horn_num, fname, freq, nx, ny, xmin, xmax, ymin, ymax, comb_data, horn_bool)
#		#modifying function not to use horn_num
#		#writegraspdata(graspoutputrep, fname, freq, nx, ny, xmin, xmax, ymin, ymax, comb_data, horn_bool)
#		#Write data with pandas
#		fname2 = os.path.basename(fname)
#		fname2 = os.path.splitext(fname2)[0]
#		PandaGraspWrite(comb_data, graspoutputrep, fname2)
#		
#		main_index += 1
#
#elif ('m' in mode) or ('M' in mode):
#	#progtype = 'MODAL'
#	#mout = modal(progtype)
#
#	#do a for loop over files
#	#but now create functions to work for one files
#
#	#there isn't much info in grasp header so skip 'readheaderinfo' func for now
#	#mdataform -> read and format modal data into array (like grasp func)
#	#return data array
#	#write header info and data in correct format
#
#	#fname = "/home/jmurphy/qbproj/x08y08.dat"
#	#rep = "/home/jmurphy/qbdataio/modaldata/"
#	files = sorted(glob.glob(modalinputrep+'*.dat'))
#	main_index = 0
#
#	for fname in files:
#		#print fname
#
#		horn_name, horn_bool = getmodalinfo(fname, main_index)
#		print horn_name, horn_bool
#
#		comb_data = mdataform(fname)
#
#		writemodaldata(modaloutputrep, comb_data, fname, horn_name, horn_bool)
#	
#		main_index += 1
#
#	#print comb_data
##End Program
