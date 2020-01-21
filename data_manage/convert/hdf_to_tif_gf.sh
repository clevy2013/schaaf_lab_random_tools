#!/bin/bash

in_dir=$1 
out_dir=$2

for hdf in $in_dir/*.hdf
do
    echo $hdf
    filename=$(basename -- $hdf)
    extension="${filename##*.}"
    filename_bare="${filename%.*}"
    gdal_translate -sds -of GTiff ${in_dir}/${filename} ${out_dir}/${filename_bare}.tif
    #gdal_translate -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MOD_Grid_BRDF:BRDF_Albedo_Band_Mandatory_Quality_shortwave ${out_dir}/${filename_bare}_qa_shortwave.tif
done
