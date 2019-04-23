#!/bin/bash

in_dir=$1 
out_dir=$2

for h5 in $in_dir/*.h5
do
    echo $h5
    filename=$(basename -- $h5)
    extension="${filename##*.}"
    filename_bare="${filename%.*}"
    # gdal_translate -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MODIS_Grid_500m_2D:sur_refl_b01_1 ${out_dir}/${filename_bare}_sr_b1.tif
    # gdal_translate -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MODIS_Grid_500m_2D:sur_refl_b02_1 ${out_dir}/${filename_bare}_sr_b2.tif
    # gdal_translate -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MODIS_Grid_500m_2D:sur_refl_b03_1 ${out_dir}/${filename_bare}_sr_b3.tif
    # gdal_translate -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MODIS_Grid_500m_2D:sur_refl_b04_1 ${out_dir}/${filename_bare}_sr_b4.tif
    # gdal_translate -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MODIS_Grid_500m_2D:sur_refl_b05_1 ${out_dir}/${filename_bare}_sr_b5.tif
    # gdal_translate -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MODIS_Grid_500m_2D:sur_refl_b06_1 ${out_dir}/${filename_bare}_sr_b6.tif
    # gdal_translate -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MODIS_Grid_500m_2D:sur_refl_b07_1 ${out_dir}/${filename_bare}_sr_b7.tif
    # gdal_translate -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MODIS_Grid_500m_2D:QC_500m_1 ${out_dir}/${filename_bare}_sr_qc.tif
    #gdal_translate -of GTiff HDF5:'"'${in_dir}/${filename}'"'://HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data_Fields/Albedo_WSA_shortwave ${out_dir}/${filename_bare}_wsa_shortwave.tif
    #gdal_translate -of GTiff HDF5:'"'${in_dir}/${filename}'"'://HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data_Fields/BRDF_Albedo_Band_Mandatory_Quality_shortwave ${out_dir}/${filename_bare}_qa_shortwave.tif
    gdal_translate -a_srs 'PROJCS["unnamed", GEOGCS["Unknown datum based upon the custom spheroid", DATUM["Not specified (based on custom spheroid)", SPHEROID["Custom spheroid",6371007.181,0]], PRIMEM["Greenwich",0], UNIT["degree",0.0174532925199433]], PROJECTION["Sinusoidal"], PARAMETER["longitude_of_center",0], PARAMETER["false_easting",0], PARAMETER["false_northing",0],UNIT["Meter",1]]' -a_ullr -8895604.15733 7783653.63767 -7783653.63767 6671703.118 -of GTiff HDF5:'"'${in_dir}/${filename}'"'://HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data_Fields/Albedo_WSA_shortwave ${out_dir}/${filename}_wsa_shortwave.tif

    gdal_translate -a_srs 'PROJCS["unnamed", GEOGCS["Unknown datum based upon the custom spheroid", DATUM["Not specified (based on custom spheroid)", SPHEROID["Custom spheroid",6371007.181,0]], PRIMEM["Greenwich",0],      UNIT["degree",0.0174532925199433]], PROJECTION["Sinusoidal"], PARAMETER["longitude_of_center",0], PARAMETER["false_easting",0], PARAMETER["false_northing",0],UNIT["Meter",1]]' -a_ullr -8895604.15733 7783653.63767 -7783653.63767 6671703.118 -of GTiff HDF5:'"'${in_dir}/${filename}'"'://HDFEOS/GRIDS/VIIRS_Grid_BRDF/Data_Fields/BRDF_Albedo_Band_Mandatory_Quality_shortwave ${out_dir}/${filename}_qa_shortwave.tif

done


