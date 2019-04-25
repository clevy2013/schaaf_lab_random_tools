#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 10:04:10 2018

@author: aelmes
"""

import numpy as np
import matplotlib.pyplot as plt
import os, glob, datetime, sys, rasterio, pyproj

in_dir = '/home/aelmes/data/above/2014/tif'
fig_dir = '/home/aelmes/data/above/'
os.chdir(in_dir)


# Set up graph days and time axis
doys = range(1, 366)
year = in_dir.split('/')[-2]

# Create empty arrays for mean, sd
wsa_swir_mean = []
wsa_swir_sd = []

for day in doys:
    # Open the shortwave white sky albedo band.
    # The list approach is because of the processing date part of the file
    # name, which necessitates the wildcard -- this was just the easiest way.

    wsa_tif_list = glob.glob(os.path.join(in_dir,'wsa','MCD43A3.A{year}{day:03d}*wsa_shortwave.tif'.format(day=day, year=year)))
    bsa_tif_list = glob.glob(os.path.join(in_dir,'bsa','MCD43A3.A{year}{day:03d}*bsa_shortwave.tif'.format(day=day, year=year)))
    qa_tif_list = glob.glob(os.path.join(in_dir,'qa','MCD43A3.A{year}{day:03d}*qa_shortwave.tif'.format(day=day, year=year)))
    
    # See if there is a raster for the date, if not use a fill value for the graph
    if len(wsa_tif_list) == 0 or len(bsa_tif_list) == 0 or len(qa_tif_list) == 0:
        #print('File not found: MCD43A3.A{year}{day:03d}*wsa_shortwave.tif'.format(day=day, year=year))
        wsa_swir_subset_flt = float('nan')
    elif len(wsa_tif_list) > 1:
        print('Multiple matching files found for same date!')
        sys.exit()
    else:
        #print('Found file: ' + ' MCD43A3.A{year}{day:03d}*wsa_shortwave.tif'.format(day=day, year=year))
        wsa_tif = wsa_tif_list[0]
        bsa_tif = bsa_tif_list[0]
        qa_tif = qa_tif_list[0]
        
    # Open tif as gdal ds but using rasterio for simplicity
        wsa_raster = rasterio.open(wsa_tif)
        qa_raster = rasterio.open(qa_tif)
        wsa_band = wsa_raster.read(1)
        qa_band = qa_raster.read(1)
    
        # Convert the lat/long point of interest to row/col
        in_proj = pyproj.Proj(init='epsg:4326')
        out_proj = pyproj.Proj(wsa_raster.crs)
        x, y = pyproj.transform(in_proj, out_proj, -178, 66)
        smp_rc = wsa_raster.index(x, y)
            
        #center = raster.xy(raster.height // 2, raster.width // 2)
    
        # Mask out nodata values
        wsa_swir_masked = np.ma.masked_array(wsa_band, wsa_band == 32767)
        wsa_swir_masked_qa = np.ma.masked_array(wsa_swir_masked, qa_band > 1)
    
        # Spatial subset based on coordinates of interest.
        wsa_swir_subset = wsa_swir_masked_qa[smp_rc]
        wsa_swir_subset_flt = np.multiply(wsa_swir_subset, 0.001)
        
        # Calculate mean and std dev
        #wsa_swir_mean.append(wsa_swir_masked.mean())
        #wsa_swir_sd.append(wsa_swir_masked.std())
        #print(wsa_swir_subset_flt)
    #print(wsa_swir_subset_flt)
    wsa_swir_mean.append(wsa_swir_subset_flt)
    

# Do plotting and save output
print(len(doys))
print(len(wsa_swir_mean))
series_name = 'Barrow FluxTower {year}'.format(year=year)
os.chdir(fig_dir)
plt.ion()
fig = plt.figure()
fig.suptitle('ABoVE Domain Albedo Time Series')
ax = fig.add_subplot(111)
fig.subplots_adjust(top=0.85)
ax.set_title(series_name)
ax.set_xlabel('DOY')
ax.set_ylabel('White Sky Albedo')
plt.xlim(0, 365)
plt.ylim(0.0, 1.0)
ax.plot(doys, wsa_swir_mean)
plt_name = str(year + '_' + series_name.replace(" ", ""))
plt.savefig('{plt_name}.png'.format(plt_name=plt_name))
