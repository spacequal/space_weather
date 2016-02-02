#!/usr/bin/env python2.7
#-*-encoding=utf-8-*-
'''
Read in summary data from Wingkp

Author: Branden Allen
Date: 140911
'''

#Numerical
import numpy as np
import pandas as pa

#Plot
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pl
from matplotlib import dates

#URL
import urllib as ul

#Time
import os
import time as tm

#####################################################################
def convert_time(val):
	try:
		v= val.split()
		return pa.Timestamp('-'.join(v[:3])+'T'+v[3][:2]+':'+v[3][2:])
	except ValueError:
		return pa.NaT

#####################################################################
#SETTINGS 
#data= 'data/wingkp_list.txt'
data= 'http://services.swpc.noaa.gov/text/wing-kp.txt'
os.environ['TZ']= 'UTC'
base_dir= os.path.join(os.environ['HOME'],'kasei0/astronomy/space_weather/NOAA')

#Label Definitions
label= [
	('UT'                ,(0  ,16 )),                 
	('status'            ,(18 ,22 )),
	('1-hour UT'         ,(23 ,39 )),
	('1-hour index'      ,(44 ,48 )),
	('1-hour lead time'  ,(55 ,59 )),
	('4-hour UT'         ,(64 ,80 )),
	('4-hour index'      ,(86 ,90 )),
	('4-hour lead time'  ,(95 ,100)),
	('Kp'                ,(108,112)),
	]
time_cols= ['UT','1-hour UT','4-hour UT']
idx= ['1-hour lead time', '4-hour lead time']

#Set up the data frame
d= pa.read_fwf(data, header= 20, 
	names= [i[0] for i in label], 
	colspecs= [i[1] for i in label])
for ii in time_cols: d[ii]= d[ii].apply(convert_time)
d= d.set_index('UT')

#Set label formats
ax= pl.gca()
df= dates.DateFormatter('%H')
dl= dates.HourLocator()
dm= dates.MinuteLocator(interval= 15)
ax.xaxis.set_major_formatter(df)
ax.xaxis.set_major_locator(dl)
ax.xaxis.set_minor_locator(dm)

#Plot the frame
pl.plot(d.index, d['Kp'])
msk= ~d['1-hour UT'].isnull()
x= d['1-hour UT'][msk]#-d['1-hour lead time'][msk].apply(pa.datetools.Minute)+pa.datetools.Hour(1)
pl.plot(x, d['1-hour index'][msk], ls= ':', color= 'black')
pl.plot(x, d['1-hour index'][msk], marker= 'o', color= 'red', ls= 'none')
msk= ~d['4-hour UT'].isnull()
x= d['4-hour UT'][msk]#-d['4-hour lead time'][msk].apply(pa.datetools.Minute)+pa.datetools.Hour(4)
pl.plot(x, d['4-hour index'][msk], color= 'black', ls= ':')
pl.plot(x, d['4-hour index'][msk], marker= 'v', color= 'brown', ls= 'none')

#Current Time
now= pa.datetime.now()
pl.plot(2*[now], [-1,10], color= 'magenta', ls= 'dashed', lw= 1.5)

#Set the labels and bounds
pl.ylim([-1,10])
pl.xlim([d.index.max()-pa.datetools.Hour(5),d.index.max()+pa.datetools.Hour(5)])
pl.xlabel('UT Hour')
pl.ylabel('Kp')
txt= tm.strftime('%Y-%m-%d %H:%M:%S ZT', now.utctimetuple())
pl.text(now-pa.datetools.Minute(3), 10, txt, 
	va= 'top', ha= 'right', rotation= 90., color= 'magenta', size= 'small')
	#bbox= {'pad':3, 'facecolor':'none', 'edgecolor':'none', textcolor:'magenta'})
pl.minorticks_on()
pl.grid()
pl.draw()

#Save figure store data
base_name= tm.strftime('%y%m%d%H%M', now.utctimetuple())
pl.savefig(os.path.join(base_dir,'figs/wingkp','%s.png'%base_name), 
	bbox_inches='tight', dpi= 600)
d.to_pickle(os.path.join(base_dir,'data/wingkp','%s.pa'%base_name))

#Store the raw text file
with open(os.path.join(base_dir,'data/wingkp','%s.txt'%base_name), 'w') as f:
	u= ul.urlopen(data)
	f.write(u.read())
	u.close()



#####################################################################


