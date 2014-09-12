#!/usr/bin/env python
#-*-encoding=utf-8-*-
'''
ACE Summary Plot

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
from lib import ace

#Standard
import StringIO
import time as tm
import urllib
import os
import re

#####################################################################
#SETTINGS
data_dir= 'data/ACE'
os.environ['TZ']= 'UTC'

#Parse all files
d= pa.concat([ace.open(os.path.join(data_dir,i)).dataframe().set_index('UT') for i in os.listdir(data_dir)])
dc= d.drop_duplicates().sort()

#Draw Bz for ACE
B= dc[['Bz','Bx','By','Bt']]
B[B== -999]= np.nan
B= B.dropna()
pl.plot(B.index, B['Bt'], color= 'blue', label= '$|\\vec{B}|$')
pl.plot(B.index, B['Bx'], color= 'black', label= '$B_x$')
pl.plot(B.index, B['By'], color= 'gray', label= '$B_y$')
pl.plot(B.index, B['Bz'], color= 'red', label= '$B_z$', lw= 1.5)

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
pl.ylim([-50,50])
pl.xlim([now-pa.datetools.Hour(9),now+pa.datetools.Hour(1)])
pl.xlabel('UT Hour')
pl.ylabel('ACE B-Field')
txt= tm.strftime('%Y-%m-%d %H:%M:%S Z', now.utctimetuple())
pl.text(0.01, 0.99, txt, va= 'top', ha= 'left', 
	color= 'magenta', transform= ax.transAxes)
pl.minorticks_on()
pl.grid()
pl.draw()

leg= pl.legend(loc= 'lower left')

#####################################################################
