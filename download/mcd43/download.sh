#!/bin/bash

dl_url=$1
file=$2
dl_dir=$3

echo "Downloading..."

wget --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --keep-session-cookies --no-check-certificate --auth-no-challenge=on -r --reject "index.html*" --accept "${file}" -l1 -np -e robots=off --no-directories --waitretry=300 -t 100 --directory-prefix=${dl_dir} --secure-protocol=TLSv1 ${dl_url}

echo "Done!"
