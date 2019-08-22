#!/bin/bash

dl_url=$1
dl_dir=$2
tile_id=$3

echo "Downloading..."
echo $dl_url

wget --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --keep-session-cookies --no-check-certificate --auth-no-challenge=on -r --reject "index.html*" --accept "*$tile_id*.hdf" -l1 -np -e robots=off --no-directories --waitretry=300 -t 100 --directory-prefix=$dl_dir --secure-protocol=TLSv1 $dl_url

echo "Done!"
