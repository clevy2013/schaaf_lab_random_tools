#!/bin/bash

dl_dir=/muddy/data05/arthur.elmes/lance
a1_dir=$dl_dir/MCD43A1
a2_dir=$dl_dir/MCD43A2
a3_dir=$dl_dir/MCD43A3
a4_dir=$dl_dir/MCD43A4
mod09_dir=$dl_dir/MOD09GA
myd09_dir=$dl_dir/MYD09GA

declare -a tiles=("h12v04" "h11v11" "h17v07" "h09v05" "h24v04" "h11v08")

# organize MCD43A1
for tile in "${tiles[@]}"
do
    rsync -av --remove-source-files $a1_dir/$tile/allData/6/MCD43A1N/Recent/ $a1_dir/$tile/
done

# organize MCD43A2
for tile in "${tiles[@]}"
do
    rsync -av --remove-source-files $a2_dir/$tile/allData/6/MCD43A2N/Recent/ $a2_dir/$tile/
done

# organize MCD43A3
for tile in "${tiles[@]}"
do
    rsync -av --remove-source-files $a3_dir/$tile/allData/6/MCD43A3N/Recent/ $a3_dir/$tile/
done

# organize MCD43A4
for tile in "${tiles[@]}"
do
    rsync -av --remove-source-files $a4_dir/$tile/allData/6/MCD43A4N/Recent/ $a4_dir/$tile/
done

# organize MOD09GA
for tile in "${tiles[@]}"
do
    rsync -av --remove-source-files $mod09_dir/$tile/allData/6/MOD09GA/Recent/ $mod09_dir/$tile/
done

# organize MYD09GA
for tile in "${tiles[@]}"
do
    rsync -av --remove-source-files $myd09_dir/$tile/allData/6/MYD09GA/Recent/ $myd09_dir/$tile/
done

