#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 10:04:10 2018

@author: aelmes

Taiga,AK,Delta Junction - DEJU,63.88112,-145.75136,Relocatable Terrestrial,Bureau of Land Management,Complete,Partially Available,h11v02
Taiga,AK,Caribou-Poker Creeks Research Watershed - BONA,65.15401,-147.50258,Core Terrestrial,University of Alaska,Complete,Partially Available,h11v02
Tundra,AK,Barrow Environmental Observatory - BARR,71.28241,-156.61936,Relocatable Terrestrial,Barrow Environmental Observatory,Complete,Partially Available,h12v01
Tundra,AK,Toolik - TOOL,68.66109,-149.37047,Core Terrestrial,Bureau of Land Management,Complete,Partially Available,h12v02
Taiga,AK,Healy - HEAL,63.87569,-149.21334,Relocatable Terrestrial,Alaska Department of Natural Resources,h11v02


"""

import numpy as np
import matplotlib.pyplot as plt
import os, glob, datetime, sys, rasterio, pyproj, csv

years = [ "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019" ]

sites_dict = {
    "DEJU" : (63.88112 -145.75136),
    "BONA" : (65.15401,-147.50258),
    "BARR" : (71.28241,-156.61936),
    "TOOL" : (68.66109,-149.37047),
    "HEAL" : (63.87569,-149.21334)
    }

def main():

in_dir = '/muddy/data01/arthur.elmes/above/2013/mcd43/h11v02/tif'
fig_dir = '/muddy/data01/arthur.elmes/above/figs/'
os.chdir(in_dir)


# Set up graph days and time axis
doys = range(1, 366)
year = in_dir.split('/')[-4]

# Set up location and coords TODO make these cli args
location="Taiga,AK,Delta Junction"
lat_long = (63.88112 ,-145.75136)

# Convert the lat/long point of interest to row/col
template_tif_list = glob.glob(os.path.join(in_dir,'wsa','MCD43A3.A{year}*wsa_shortwave.tif'.format(year=year)))
template_tif = template_tif_list[0]
template_raster = rasterio.open(template_tif)
in_proj = pyproj.Proj(init='epsg:4326')
out_proj = pyproj.Proj(template_raster.crs)
x, y = pyproj.transform(in_proj, out_proj, lat_long[1], lat_long[0])
smp_rc = template_raster.index(x, y)
print("Querying pixel:" + str(smp_rc))

#center = raster.xy(raster.height // 2, raster.width // 2)


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
#print(*doys)
#print(*wsa_swir_mean)
series_name = location + " " + str(year)
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
print('Saving plot to: ' + '{plt_name}.png'.format(plt_name=plt_name))
plt.savefig('{plt_name}.png'.format(plt_name=plt_name))

csv_name = str(series_name + ".csv")
# export data to csv
with open(csv_name, "w") as export_file:
    wr = csv.writer(export_file, dialect='excel', lineterminator='\n')
    for day in wsa_swir_mean:
        wr.writerow([day])


if __name__ == "__main__":
    main()
