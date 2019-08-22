#!/bin/bash

## Feeds the download feeder with years and tiles. probably should combine these scripts into one, but hey, it's temporary.
## afme

file=./above_tiles_plots.txt

file_lines=`cat $file`
echo "Start"
for year in $(seq 2015 2019); do
    for line in $file_lines; do
	echo  ${year}-01-01 $line 3
	./feed_download_mcd43_rev3.sh ${year}-01-01 $line 3 
    done
done
