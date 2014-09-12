#!/usr/bin/env python
#-*-encoding=utf-8-*-
'''
GOES Summary Plot

Author: Branden Allen
Date: 140912
'''
from __future__ import print_function

#Numerical
import numpy as np
import pandas as pa

#Plotting
import matplotlib.pyplot as pl
from matplotlib import dates

#Local
from lib import goes

#Standard
import StringIO
import time as tm
import urllib
import os
import re

#####################################################################
#SETTINGS
data_dir= 'data/GOES'
os.environ['TZ']= 'UTC'

#Parse all files
for sat in ['Gp','Gs']:
	pl.figure()
	d= pa.concat([goes.open(os.path.join(data_dir,i)).dataframe().set_index('UT') for i in os.listdir(data_dir) if re.search(sat,i)])
	dc= d.drop_duplicates().sort()

	#Draw Bz for ACE
	B= dc[['He','Hn','Hp','total field']]
	B[B== 100000.0]= np.nan
	B= B.dropna()
	pl.plot(B.index, B['total field'], color= 'blue', label= '$|\\vec{H}|$')
	pl.plot(B.index, B['He'], color= 'black', label= '$H_e$')
	pl.plot(B.index, B['Hn'], color= 'gray', label= '$H_n$')
	pl.plot(B.index, B['Hp'], color= 'red', label= '$H_p$', lw= 1.5)

	#Set label formats
	ax= pl.gca()
	df= dates.DateFormatter('%H')
	dl= dates.HourLocator()
	dm= dates.MinuteLocator(interval= 15)
	ax.xaxis.set_major_formatter(df)
	ax.xaxis.set_major_locator(dl)
	ax.xaxis.set_minor_locator(dm)

	#Current Time
	now= pa.datetime.now()

	#Set the labels and bounds
	pl.ylim([-50,350])
	pl.xlim([now-pa.datetools.Hour(9),now+pa.datetools.Hour(1)])
	pl.xlabel('UT Hour')
	pl.ylabel('GOES H-Field')
	txt= tm.strftime('%Y-%m-%d %H:%M:%S Z', now.utctimetuple())
	pl.text(0.01, 0.99, txt, va= 'top', ha= 'left', 
		color= 'magenta', transform= ax.transAxes)
	pl.minorticks_on()
	pl.grid()
	pl.draw()

	leg= pl.legend(loc= 'lower left')

#####################################################################
