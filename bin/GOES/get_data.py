#!/usr/bin/env python
#-*-encoding=utf-8-*-
'''
GOES SWPC data retrieval

Author: Branden Allen
Date: 140912
'''
from __future__ import print_function

#Numerical
import pandas as pa

#Standard
import time as tm
import os, re, urllib

#####################################################################
#SETTINGS
base_url= 'http://www.swpc.noaa.gov/ftpdir/lists'
data_list= [
	('pchan/Gp_pchan_5m.txt'    ,      '5 min GOES-13 Energetic Proton Data'),
	('pchan/Gs_pchan_5m.txt'    ,      '5 min GOES-15 Energetic Proton Data'),
	('xray/Gp_xr_1m.txt'        ,      '1 min GOES-13 X-Ray Data'           ),
	('xray/Gs_xr_1m.txt'        ,      '1 min GOES-15 X-Ray Data'           ),
	('geomag/Gp_mag_1m.txt'     ,      '1 min GOES-13 Magnetometer Data'    ),
	('geomag/Gs_mag_1m.txt'     ,      '1 min GOES-15 Magnetometer Data'    ),
	('particle/Gp_part_5m.txt'  ,      '5 min GOES-13 Particle Data'        ),
	('particle/Gs_part_5m.txt'  ,      '5 min GOES-15 Particle Data'        ),
	('ace/ace_epam_5m.txt'      ,      'ACE e/p alpha monitor'              ),
	('ace/ace_mag_1m.txt'       ,      ''                                   ),
	('ace/ace_sis_5m.txt'       ,      ''                                   ),
	('ace/ace_swepam_1m.txt'    ,      ''                                   ),
	]
base_dir= os.path.join(os.environ['HOME'],'kasei0/astronomy/space_weather/NOAA')
goes_out_dir= os.path.join(base_dir, 'data/GOES')
ace_out_dir= os.path.join(base_dir, 'data/ACE')

#Get the current time and encode a base filename
os.environ['TZ']= 'UTC'
now= pa.datetime.now()
base_name= tm.strftime('%y%m%d%H%M', now.utctimetuple())

#Retrieve all files
for fname, description in data_list:
	out_name= base_name+'.'+os.path.basename(fname)

	#Select satellite output
	if re.search('ace',fname):
		out_dir= ace_out_dir
	else:
		out_dir= goes_out_dir

	with open(os.path.join(out_dir, out_name), 'w') as f: 
		u= urllib.urlopen(os.path.join(base_url,fname))
		f.write(u.read())
		u.close()

#####################################################################
#                                                                   #
#                                                                   #
#                                                                   #
#####################################################################
