#!/usr/bin/env python
#-*-encoding=utf-8-*-
'''
NOAA Data Analysis Library

Author: Branden Allen
Date: 140912
'''
from __future__ import print_function

#Numerical
import numpy as np
import pandas as pa

#Standard
import StringIO
import time as tm
import urllib
import os
import re

#####################################################################
class noaa_file(object):
	'''
	Data parser for NOAA summary files.

	Parameters
	----------
	file_name: string
		The data file path
	'''
	def __init__(self, file_name, *args, **kargs):
		super(noaa_file,self).__init__(*args, **kargs)
		self.file_name= file_name

		#Read in the data file
		with open(file_name,'r') as f: self.data= f.read()

		#Search for the last comment marker then exclude the final comment line
		pos= [ii.end() for ii in re.finditer('#',self.data)]
		d= self.data[pos[-1]:]
		d= d[re.search('\n',d).end():]
		self.main_data= d

	def set_col_defs(self, names, colspecs, time_cols= None):
		'''
		Set the column definitions for data parsing

		Paramters
		---------
		names: list [name0, ...]
			A list containing a single string for each column label
		colspecs: list [(start,stop), ...]
			A list of tuples containing the start and stop positions
			of each column in the raw data file.
		time_cols: list [name0, ...]
			A list of column names which to be reformatted as timestamps
		'''
		self.names= names
		self.colspecs= colspecs
		self.time_cols= time_cols

	def dataframe(self):
		'''
		Parse the text file and return the data frame

		Returns
		-------
		data_table: pa.DataFrame
			A formated output dataframe containing the file data
		'''
		#FWF parsing
		df= pa.read_fwf(StringIO.StringIO(self.main_data), 
			names= self.names, 
			colspecs= self.colspecs)

		#Conversion to machine readable timestamps
		if self.time_cols!= None:
			def convert_time(val):
				try:
					v= val.split()
					return pa.Timestamp('-'.join(v[:3])+'T'+v[3][:2]+':'+v[3][2:])
				except ValueError:
					return pa.NaT
			for ii in self.time_cols: df[ii]= df[ii].apply(convert_time)

		#Final parsed data frame
		return df

#####################################################################

