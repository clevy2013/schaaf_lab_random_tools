#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 10:04:10 2018

@author: aelmes
"""

import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal
import os, glob, datetime

os.chdir('/home/aelmes/Data/test/tif/')

plt.ion()

# Set up graph days and time axis
doys = range(182, 213)
#t_axis = np.array([datetime.datetime(2018, 7, i, 0) for i in range(1,doys)])

#for year in range(2017, 2019):
#    for doy in range(1, 366):
#        days.append(str(year) + str(doy))


# Create empty arrays for mean, sd
alb_swir_mean = []
alb_swir_sd = []

for day in doys:
    tif_list = glob.glob('MCD43A3.A2018%03d.h16v01.006.*_Albedo_BSA_shortwave.tif' % day)
    if len(tif_list) == 0:
        print('File not found: MCD43A3.A2018%03d.h16v01.006.*_Albedo_BSA_shortwave.tif' % day)
        pass
    else:
        tif = tif_list[0]
    # Open tif as gdal ds
    g = gdal.Open(tif)

    # Open gdal ds band 1 as np array (only 1 band because of previous convert
    # from hdf to tif using MRT/pyModis)
    alb_swir = g.GetRasterBand(1).ReadAsArray()
    
    alb_swir_masked = np.ma.masked_array(alb_swir, alb_swir == 32767)

    # Calculate mean and std dev
    alb_swir_mean.append(alb_swir_masked.mean())
    alb_swir_sd.append(alb_swir_masked.std())

#plt.plot(doys, alb_swir_mean

fig = plt.figure()
fig.suptitle('Greenland Albedo Time Series')
ax = fig.add_subplot(111)
fig.subplots_adjust(top=0.85)
ax.set_title('Test Run')
ax.set_xlabel('2018 Julian DOY')
ax.set_ylabel('Black Sky Albedo')
ax.plot(doys, alb_swir_mean)
plt.show()
