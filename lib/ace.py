#!/usr/bin/env python
#-*-encoding=utf-8-*-
'''
ACE data anlysis library

Author: Branden Allen
Date: 140912
'''
from __future__ import print_function

#Numerical
import numpy as np
import pandas as pa

#Library
import lib

#Standard
import StringIO
import time as tm, urllib, os, re

#####################################################################
def open(file_name):
	'''
	Return the appropriate file object based on a pattern match from 
	the input filename

	Parameters
	----------
	file_name: string
		Path to the input data file
	
	Returns
	-------
	data_file: lib.noaa_file (subclass)
		Returns the appropriate data parser with the file loaded
	'''
	if re.search('ace_epam',file_name):
		return epam_file(file_name)
	elif re.search('ace_mag',file_name):
		return mag_file(file_name)
	elif re.search('ace_sis',file_name):
		return sis_file(file_name)
	elif re.search('ace_swepam',file_name):
		return swepam_file(file_name)
	else:
		raise TypeError

class mag_file(lib.noaa_file):
	def __init__(self, file_name, *args, **kargs):
		super(mag_file, self).__init__(file_name, *args, **kargs)

		#Column Definitions
		label= [
			('UT'                    ,(0  ,16 )),                 
			('MJD'                   ,(19 ,26 )),
			('seconds of the day'    ,(27 ,32 )),
			('S'                     ,(36 ,37 )),
			('Bx'                    ,(39 ,45 )),
			('By'                    ,(47 ,53 )),
			('Bz'                    ,(55 ,60 )),
			('Bt'                    ,(63 ,68 )),
			('lat'                   ,(71 ,76 )),
			('lon'                   ,(79 ,84 )),
			]
		self.names= [i[0] for i in label]
		self.colspecs= [i[1] for i in label]
		self.time_cols= ['UT']

class sis_file(lib.noaa_file):
	def __init__(self, file_name, *args, **kargs):
		super(sis_file, self).__init__(file_name, *args, **kargs)

		#Column Definitions
		label= [
			('UT'                    ,(0  ,16 )),                 
			('MJD'                   ,(20 ,27 )),
			('seconds of the day'    ,(28 ,33 )),
			('S1'                    ,(39 ,40 )),
			('>10 MeV'               ,(43 ,52 )),
			('S2'                    ,(56 ,57 )),
			('>30 MeV'               ,(60 ,69 )),
			]
		self.names= [i[0] for i in label]
		self.colspecs= [i[1] for i in label]
		self.time_cols= ['UT']

class swepam_file(lib.noaa_file):
	def __init__(self, file_name, *args, **kargs):
		super(swepam_file, self).__init__(file_name, *args, **kargs)

		#Column Definitions
		label= [
			('UT'                    ,(0  ,16 )),                 
			('MJD'                   ,(18 ,24 )),
			('seconds of the day'    ,(27 ,32 )),
			('S'                     ,(36 ,38 )),
			('proton density'        ,(40 ,48 )),
			('bulk speed'            ,(51 ,59 )),
			('ion temperature'       ,(62 ,72 )),
			]
		self.names= [i[0] for i in label]
		self.colspecs= [i[1] for i in label]
		self.time_cols= ['UT']

class epam_file(lib.noaa_file):
	def __init__(self, file_name, *args, **kargs):
		super(epam_file, self).__init__(file_name, *args, **kargs)

		#Column Definitions
		label= [
			('UT'                    ,(0  ,16 )),                 
			('MJD'                   ,(19 ,24 )),
			('seconds of the day'    ,(27 ,32 )),
			('electron S'            ,(33 ,35 )),
			('electron 38-53'        ,(36 ,45 )),
			('electron 175-315'      ,(46 ,55 )),
			('proton S'              ,(56 ,58 )),
			('proton 47-68'          ,(59 ,68 )),
			('proton 115-195'        ,(69 ,78 )),
			('proton 310-580'        ,(79 ,88 )),
			('proton 795-1193'       ,(89 ,98 )),
			('proton 1060-1900'      ,(99 ,108)),
			('anis. index'           ,(110,115)),
			]
		self.names= [i[0] for i in label]
		self.colspecs= [i[1] for i in label]
		self.time_cols= ['UT']

#####################################################################

