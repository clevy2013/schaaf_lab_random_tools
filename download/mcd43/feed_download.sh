#!/bin/bash

# Call downloader script with 5 args: start date (YYYY-MM-DD); end date (YYYY-MM-DD); product short name (e.g. MCD43A1 -- works with SR and Albedo products as is); tile; download dir
# start_date=$1
# end_date=$2
# short_name=$3
# tile=$4
# dl_dir=$5

url_base=https://e4ftl01.cr.usgs.gov/

usage="Usage: cmd [-s start date] [-e end date] [-n product short name] [-t tile] [-d download dir]"
while getopts ":s:e:n:t:d:" arg; do
    case $arg in
	s) start_date=$OPTARG;;
	e) end_date=$OPTARG;;
	n) short_name=$OPTARG;;
	t) tile=$OPTARG;;
	d) dl_dir=$OPTARG;;
	\?) echo $usage
    esac
done

if [ -z $start_date ] || [ -z $end_date ] || [ -z $short_name ] || [ -z $tile ] || \
       [ -z $dl_dir ]; then
    echo $usage
    exit
else
    echo "All ok"
fi

# Check which product was specified to select the right URL
case ${short_name} in
    "MOD09GA") echo "Found Terra SR"
	       url_prod=${url_base}"MOLT/${short_name}.006/";;
    "MYD09GA") echo "Found Aqua SR"
	       url_prod=${url_base}"MOLA/${short_name}.006/";;
    "MCD43A1"|"MCD43A2"|"MCD43A3"|"MCD43A4") echo "Found Combeind Albedo"
	       url_prod=${url_base}"MOTA/${short_name}.006/";;
esac

cur_date=${start_date}
end_date=$(date -I -d "$end_date+1 day")

# Loop through all dates in year, pass to download script with full url
while [[ "$cur_date" < "$end_date" ]]; do 
    dl_dir_out=$dl_dir
    cur_date_url=${cur_date:0:4}.${cur_date:5:2}.${cur_date:8:2}
    dl_url=${url_prod}${cur_date_url}/
    file="${short_name}*${tile}*.hdf"
    cur_date=$(date -I -d "$cur_date+1 day")
    year=`date --date="$cur_date" '+%Y'`
    dl_dir_out=${dl_dir_out}${short_name}/hdf/${year}/${tile}
    if [ ! -r $dl_dir_out ]; then
	mkdir -p $dl_dir_out
    fi
    echo "Downloading from:" ${dl_url}
    echo "File: " ${file}
    echo "Saving to: " ${dl_dir_out}
    bash ./download.sh ${dl_url} ${file} ${dl_dir_out}
done
