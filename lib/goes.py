#!/usr/bin/env python
#-*-encoding=utf-8-*-
'''
GOES data anlysis library

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
import time as tm
import urllib
import os
import re

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
	if re.search('_xr_',file_name):
		return xr_file(file_name)
	elif re.search('_mag_',file_name):
		return mag_file(file_name)
	elif re.search('_pchan_',file_name):
		return pchan_file(file_name)
	elif re.search('_part_',file_name):
		return part_file(file_name)
	else:
		raise TypeError

class pchan_file(lib.noaa_file):
	def __init__(self, file_name, *args, **kargs):
		super(pchan_file, self).__init__(file_name, *args, **kargs)

		#Column Definitions
		label= [
			('UT'                    ,(0  ,16 )),                 
			('MJD'                   ,(18 ,25 )),
			('seconds of the day'    ,(26 ,31 )),
			]
		label+= [('P%d'%i, (33+(i-1)*10, 41+(i-1)*10)) for i in xrange(1,12)]
		self.names= [i[0] for i in label]
		self.colspecs= [i[1] for i in label]
		self.time_cols= ['UT']

class part_file(lib.noaa_file):
	def __init__(self, file_name, *args, **kargs):
		super(part_file, self).__init__(file_name, *args, **kargs)

		#Column Definitions
		label= [
			('UT'                    ,(0  ,16 )),                 
			('MJD'                   ,(19 ,24 )),
			('seconds of the day'    ,(26 ,31 )),
			]
		label+= [('P>%.1f'%i, (33+n*10, 42+n*10))  for n,i in enumerate([1,5,10,30,50,100])]
		label+= [('E>%.1f'%i, (94+n*10, 102+n*10)) for n,i in enumerate([0.8, 2.0, 4.0])]
		self.names= [i[0] for i in label]
		self.colspecs= [i[1] for i in label]
		self.time_cols= ['UT']

class xr_file(lib.noaa_file):
	def __init__(self, file_name, *args, **kargs):
		super(xr_file, self).__init__(file_name, *args, **kargs)

		#Column Definitions
		label= [
			('UT'                    ,(0  ,16 )),                 
			('MJD'                   ,(19 ,24 )),
			('seconds of the day'    ,(26 ,31 )),
			('ls'                    ,(36 ,44 )),
			('lw'                    ,(48 ,56 )),
			]
		self.names= [i[0] for i in label]
		self.colspecs= [i[1] for i in label]
		self.time_cols= ['UT']

class mag_file(lib.noaa_file):
	def __init__(self, file_name, *args, **kargs):
		super(mag_file, self).__init__(file_name, *args, **kargs)

		#Column Definitions
		label= [
			('UT'                    ,(0  ,16 )),                 
			('MJD'                   ,(19 ,24 )),
			('seconds of the day'    ,(26 ,31 )),
			('Hp'                    ,(36 ,44 )),
			('He'                    ,(48 ,56 )),
			('Hn'                    ,(60 ,68 )),
			('total field'           ,(72 ,80 )),
			]
		self.names= [i[0] for i in label]
		self.colspecs= [i[1] for i in label]
		self.time_cols= ['UT']

#####################################################################
