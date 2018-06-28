from glob import glob
import os

# Set relevant dirs
#wk_dir = os.path.dirname(os.path.realpath(__file__))
wk_dir = '/media/sf_LinuxShare/outputsTest'

# Set year, band list, product list
year = '2000'
band_list = [1, 2, 3, 4, 5, 6, 7]
prod_list = ['bsa', 'geo', 'iso', 'nbar', 'qa', 'vol', 'wsa']

# Set up complete dictionary of products
hdf_dict = {}
for prod in prod_list:
    for band in band_list:
        for i in range(1, 367):
            if i < 10:
                doy = '00' + str(i)
            elif i < 100:
                doy = '0' + str(i)
            else:
                doy = str(i)
            hdf_dict[prod + '_band' + str(band) + '_' + str(i)] = 'MCD43GF_' + prod + '_Band' + str(band) + \
                                                                  '_' + doy + '_' + year + '_V006.hdf'
print(hdf_dict)

# Loop through each *.hdf file and make sure each band/product/year has every DOY accounted for, if not
# spit it out in an errors file. This uses the ideal dictionary created above
for hdf in os.listdir(wk_dir):
    if os.path.isfile(os.path.join(wk_dir, hdf)):
        if hdf in hdf_dict.values():
            print(hdf)