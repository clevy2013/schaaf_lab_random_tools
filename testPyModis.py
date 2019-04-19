#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 13:27:21 2018

@author: aelmes
"""

import os, glob
#from IPython.core.display import Image
from pymodis import downmodis
#from pymodis import parsemodis
from pymodis.convertmodis_gdal import convertModisGDAL


# Destination folder 
dest_folder = "/home/aelmes/Data/test/"

# Tiles to download
tiles = "h16v01" #,h17v01"

# Starting day
start_day = "2018-09-20"

# Number of days to download
delta = 263

# Initialize the downmodis object
modis_down = downmodis.downModis(destinationFolder=dest_folder, tiles=tiles, 
                                 today=start_day, delta=delta, 
                                 url = "https://e4ftl01.cr.usgs.gov",
                                 path = "MOTA",
                                 product = "MCD43A3.006"
                                 )
# Actually do the downloading
modis_down.connect()
modis_down.downloadsAllDay()

# Create a list of files to use
file_list = glob.glob(os.path.join(dest_folder, 'MCD43A3.A2018*.hdf'))
print(file_list)

# Convert from hdf to tif
# First choose the layer of interest
subset = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 
          0, 0, 0, 0,  0, 0, 0, 0, 0]

# Then loop through all downloaded hdf files and convert to tif
for hdf in file_list:
    pth_parts = hdf.split("/")
    output_prefix = os.path.join("/", pth_parts[1], pth_parts[2], 
                                 pth_parts[3], pth_parts[4], "tif", 
                                 pth_parts[5][:-4])
    convert_hdf = convertModisGDAL(hdfname=hdf, prefix=output_prefix, 
                                 subset=subset, res = 500, epsg = 6974)
    convert_hdf.run()

# Parse the data
#modis_multi_parse = parsemodis.parseModisMulti(file_list)
#
## Get the value of the boundary
##modis_multi_parse.valBound()
##modis_multi_parse.boundary
#
## Create a mosaic file using layer ID 19 (zero indexed so the 20th)

#output_prefix = os.path.join(dest_folder, 'MCD43A3.A2018006.mosaic')
#output_tif = os.path.join(dest_folder, 'MCD43A3.A2018006.mosaic.tif')
#
## temporary list of files to mosaic based on shared date
#mosaic_file_list = glob.glob(os.path.join(dest_folder,'MCD43A3.A2018006*.hdf'))
#
## The first parameter is a list with the original tiles,
## the second one is a list with the subset to process,
## the last one is the output format, e.g. GTiff
#mosaic = createMosaicGDAL(mosaic_file_list, subset, 'GTiff')
#mosaic.run(output_tif)
#mosaic.write_vrt(output_prefix)
