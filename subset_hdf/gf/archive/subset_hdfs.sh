#!/bin/bash

in_dir=$1
out_dir=$2

hdfs=${in_dir}/*bsa*.hdf

for hdf in $hdfs
do
    echo "Processing $hdf"
    echo "Outputting to $out_dir"
    filename=$(basename -- $hdf)
    extension="${filename##*.}"
    filename_bare="${filename%.*}"
    gdalwarp --config CENTER_LONG 180 -t_srs '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs' -te 63 -55 210 30 -tr 0.05 0.05 -of netCDF $hdf ${out_dir}/${filename_bare}.nc
    gdalwarp -tr 0.05 0.05 -r bilinear -of netCDF ${out_dir}/${filename_bare}.nc ${out_dir}/${filename_bare}_subset.nc
    rm ${out_dir}/${filename_bare}.nc
    #gdalwarp --config CENTER_LONG 180 -t_srs '+proj=longlat +ellps=clrk66 +no_defs' -te 63 -55 210 30 -of HDF4Image $hdf ${filename_bare}.hdf 
    #gdalwarp -r bilinear -tr 0.05 0.05 -t_srs '+proj=longlat +ellps=clrk66 +no_defs' -of HDF4Image ${filename_bare}.hdf ${out_dir}/${filename_bare}_subset.hdf
done
