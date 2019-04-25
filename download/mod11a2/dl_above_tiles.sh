#!/bin/bash

## Feeds the download feeder with years and tiles. probably should combine these scripts into one, but hey, it's temporary.
## afme

in_dir=$1
out_dir=$2
file=./above_tiles.txt

file_lines=`cat $file`
echo "Start"
for year in $(seq 2012 2019); do
    for line in $file_lines; do
	echo  ${year}-01-01 ${year}-12-31 $line
	./feed_download_mod11a2.sh ${year}-01-01 ${year}-12-31 $line 
    done
done
