#!/bin/bash

## WARNING: Currently only works with tile h10v02 because of the output bounding coordinates, which must be passed in manually in meters from the origin, since for some reason gdal can't handle lat/long.
## TODO convert bounding coordinates from ll to meters so this is automated. Shortcut/hurry mode, jsut write them down in file for all above tiles, use as needed from (dictionary??)

in_dir=$1 
out_dir=$2

if [ ! -d ${out_dir} ]; then
    mkdir ${out_dir}
fi

if [ ! -d ${out_dir}/qa/ ]; then
    mkdir ${out_dir}/qa/
fi

if [ ! -d ${out_dir}/wsa/ ]; then
    mkdir ${out_dir}/wsa/
fi

if [ ! -d ${out_dir}/bsa/ ]; then
    mkdir ${out_dir}/bsa/
fi
  
for h5 in $in_dir/*.h5
do
    echo $h5
    filename=$(basename -- $h5)
    extension="${filename##*.}"
    filename_bare="${filename%.*}"
    gdal_translate -a_nodata 32767 -a_srs 'PROJCS["unnamed", GEOGCS["Unknown datum based upon the custom spheroid", DATUM["Not specified (based on custom spheroid)", SPHEROID["Custom spheroid",6371007.181,0]], PRIMEM["Greenwich",0], UNIT["degree",0.0174532925199433]], PROJECTION["Sinusoidal"], PARAMETER["longitude_of_center",0], PARAMETER["false_easting",0], PARAMETER["false_northing",0],UNIT["Meter",1]]' -a_ullr -8895604.15733 7783653.63767 -7783653.63767 6671703.118 -of GTiff HDF5:'"'${in_dir}/${filename}'"'://HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data_Fields/Albedo_WSA_shortwave ${out_dir}/wsa/${filename}_wsa_shortwave.tif

    gdal_translate -a_nodata 32767 -a_srs 'PROJCS["unnamed", GEOGCS["Unknown datum based upon the custom spheroid", DATUM["Not specified (based on custom spheroid)", SPHEROID["Custom spheroid",6371007.181,0]], PRIMEM["Greenwich",0], UNIT["degree",0.0174532925199433]], PROJECTION["Sinusoidal"], PARAMETER["longitude_of_center",0], PARAMETER["false_easting",0], PARAMETER["false_northing",0],UNIT["Meter",1]]' -a_ullr -8895604.15733 7783653.63767 -7783653.63767 6671703.118 -of GTiff HDF5:'"'${in_dir}/${filename}'"'://HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data_Fields/Albedo_BSA_shortwave ${out_dir}/bsa/${filename}_bsa_shortwave.tif
    
    gdal_translate -a_nodata 255 -a_srs 'PROJCS["unnamed", GEOGCS["Unknown datum based upon the custom spheroid", DATUM["Not specified (based on custom spheroid)", SPHEROID["Custom spheroid",6371007.181,0]], PRIMEM["Greenwich",0],      UNIT["degree",0.0174532925199433]], PROJECTION["Sinusoidal"], PARAMETER["longitude_of_center",0], PARAMETER["false_easting",0], PARAMETER["false_northing",0],UNIT["Meter",1]]' -a_ullr -8895604.15733 7783653.63767 -7783653.63767 6671703.118 -of GTiff HDF5:'"'${in_dir}/${filename}'"'://HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data_Fields/BRDF_Albedo_Band_Mandatory_Quality_shortwave ${out_dir}/qa/${filename}_qa_shortwave.tif

done


