#!/bin/bash
## Feeds the download feeder with years and tiles. probably should combine these scripts into one, but hey, it's temporary.
## afme                                                                                                   
                                                                                                          
in_dir=$1                                                                                                 
#out_dir=$2                                                                                                
file=./above_tower_tiles.txt                                                                                   

file_lines=`cat $file`
echo "Start"
for year in $(seq 2019 2019); do
    for line in $file_lines; do
        echo ${in_dir}${year}/vnp43ma3/${line}
        echo ${in_dir}${year}/vnp43ma3/${line}/tif
        ./h5_to_tif_wsa.sh ${in_dir}${year}/vnp43ma3/${line} ${in_dir}${year}/vnp43ma3/${line}/tif
    done
done
