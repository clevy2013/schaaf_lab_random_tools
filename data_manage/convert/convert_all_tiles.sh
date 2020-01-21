#!/bin/bash
## Feeds the download feeder with years and tiles. probably should combine these scripts into one, but hey, it's temporary.
## afme                                                                                                   
                                                                                                          
in_dir=$1                                                                                                 
#out_dir=$2                                                                                                
file=./above_tiles.txt                                                                                   

file_lines=`cat $file`
echo "Start"
for year in $(seq 2018 2019); do
    for line in $file_lines; do
        echo ${in_dir}${year}/mcd43a/${line}
        echo ${in_dir}${year}/mcd43a/${line}/tif
        ./hdf_to_tif_rev2.sh ${in_dir}${year}/mcd43a/${line} ${in_dir}${year}/mcd43a/${line}/tif
    done
done
