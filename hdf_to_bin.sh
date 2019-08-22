#!/bin/bash

in_dir=$1 
out_dir=$2

in_dir_wsa=${in_dir}/wsa
in_dir_bsa=${in_dir}/bsa
in_dir_qa=${in_dir}/qa

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

for tif in $in_dir_wsa/*.tif
do
    echo $tif
    filename=$(basename -- $tif)
    extension="${filename##*.}"
    filename_bare="${filename%.*}"
    gdal_translate -of ENVI ${in_dir_wsa}/${filename} ${out_dir}/wsa/${filename_bare}_wsa_shortwave.bin
    #gdal_translate -of ENVI ${in_dir}/${filename} ${out_dir}/bsa/${filename_bare}_bsa_shortwave.bin
    #gdal_translate -of ENVI ${in_dir}/${filename} ${out_dir}/qa/${filename_bare}_qa_shortwave.bin
done
