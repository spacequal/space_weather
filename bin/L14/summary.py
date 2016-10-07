#!/usr/bin/env python
#-*-encoding=utf-8-*-
'''
Summary Plots and Test Plotting Procedures for L+14 Data

Author: Branden Allen
Date: 2016.10.07
'''
from __future__ import print_function

#Numerical
import numpy as np
import pandas as pa

#Plotting
import matplotlib.pyplot as pl

#Standard
import StringIO as sio
import os
import re

#Solar Python
from sunpy.instr import goes
from astropy import units

#####################################################################
# Data Retrieval
def read_csv(filename):
	with open(filename, 'r') as f: 
		buf= f.read()
		idx= [i.end() for i in re.finditer('data:',buf)]
		d= pa.read_csv(sio.StringIO(buf[idx[0]:]))

		#Quality Flag Filter and Flux Factor Application
		d= d[d['A_QUAL_FLAG']&d['B_QUAL_FLAG']== 0]
		d['A_FLUX']/= 0.85
		d['B_FLUX']/= 0.7

		#Calculate the emission measure and temperature
		satellite= int(re.findall(':satellite_id = "GOES-(\d+)"',buf)[0])
		r= d['A_FLUX']/d['B_FLUX']
		bf,af= [units.Quantity(d[i], unit= 'W/m/m') for i in ['B_FLUX', 'A_FLUX']]
		r= af/bf
		msk= (r>2.43e-6)&(r<0.694)
		d['T [MK]']= np.nan
		d['Emission Measure [1/cm2]']= np.nan
		if np.sum(msk)!= 0:
			em= goes._goes_chianti_tem(bf[msk], af[msk], satellite= satellite)
			d['T [MK]'][msk]= em[0].value
			d['Emission Measure [1/cm2]'][msk]= em[1].value

		#Time Tag Indexing
		d['Time [UT]']= d['time_tag'].apply(pa.Timestamp)
		return d.set_index('Time [UT]')

#Extract data and plot the GOES derived temperatures for all monitors
base_name= '_xrs_2s_20160921_20160921.csv'
data_dir= 'data/GOES_full'
data= dict([('g'+repr(i),read_csv(os.path.join(data_dir,'g'+repr(i)+base_name))) for i in xrange(13,16)])
data= pa.concat(data, 1)
data= data.swaplevel(0,1,1)
data['T [MK]'].plot(ls= 'none', marker= '.')

#####################################################################

