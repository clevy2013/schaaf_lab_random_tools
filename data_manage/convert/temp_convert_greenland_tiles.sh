#!/bin/bash

in_dir=/muddy/data01/arthur.elmes/mcd43_ops/MCD43A3/
out_dir=/muddy/data01/arthur.elmes/mcd43_ops_tif/MCD43A3/

tiles="h14v00 h14v02 h15v00 h15v02 h16v00 h16v02 h17v00 h17v02 h18v00 h14v01 h14v03 h15v01 h15v03 h16v01 h16v03 h17v01 h17v03"

for tile in $tiles ; do
    echo "Processing: " ${in_dir}${tile}
    echo "Writing to: " ${out_dir}${tile}
    ./hdf_to_tif_rev2.sh ${in_dir}${tile} ${out_dir}${tile}
done

#./hdf_to_tif_rev2.sh /muddy/data01/arthur.elmes/mcd43_ops/MCD43A3/h14v01/ 
