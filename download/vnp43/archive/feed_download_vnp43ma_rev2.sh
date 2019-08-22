#!/bin/bash

#TODO add args for end date, and which prduct number and tile you want and then change corresponding download.sh to intake the tile number

# Pass in the yyyy as arg1
start_date=$1 #2014-01-01 #${1}-01-01
end_date=$2 #2014-12-31 #$(date -I -d "$start_date+1 year")
cur_date=$start_date

url_base=https://e4ftl01.cr.usgs.gov/VIIRS/VNP43MA3
vers=.001

dl_dir=/muddy/data01/arthur.elmes/above/${start_date:0:4}/vnp43ma

echo $dl_dir
#echo $start_date
#echo $end_date

# Loop through all dates in year, pass to download script with full url
while [[ "$cur_date" < "$end_date" ]]; do
    cur_date_url=${cur_date:0:4}.${cur_date:5:2}.${cur_date:8:2}
    dl_url=${url_base}${i}${vers}/${cur_date_url}
    cur_date=$(date -I -d "$cur_date+1 day")
    echo $dl_url
    if [ ! -r $dl_dir ]; then
	mkdir -p $dl_dir
    fi
    bash ./download.sh $dl_url $dl_dir
done
