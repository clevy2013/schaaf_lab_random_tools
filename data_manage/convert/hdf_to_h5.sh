#!/bin/bash

in_dir=$1 
out_dir=$2

if [ ! -d ${out_dir} ]; then
    mkdir ${out_dir}
fi

for h5 in $in_dir/*.h5
do
    echo $h5
    filename=$(basename -- $h5)
    extension="${filename##*.}"
    filename_bare="${filename%.*}"
    echo ${in_dir}/${filename} ${out_dir}/${filename_bare}.hdf
    #gdal_translate -of HDF4Image -sds ${in_dir}/${filename} ${out_dir}/${filename_bare}.hdf
done
