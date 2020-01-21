#!/home/arthur.elmes/software/anaconda3/envs/geo/bin/python

import os, glob, matplotlib, math, sys
import matplotlib.pyplot as plt
from matplotlib import cm
from sklearn.metrics import mean_squared_error
import numpy as np
import pandas as pd
import rasterio as rio

matplotlib.rcParams['agg.path.chunksize'] = 100000

# Set workspace IO dirs
workspace = "/muddy/data04/arthur.elmes/"
os.chdir(workspace)

tile1_fname_wsa = sys.argv[1] # e.g.: MCD43A3.A2018010.h09v05.061.2019344214951_wsa_shortwave.tif
tile2_fname_wsa = sys.argv[2] # e.g.: MCD43A3.A2018010.h09v05.006.2018019024815_wsa_shortwave.tif

print(tile1_fname_wsa)
print(tile2_fname_wsa)

tile = tile1_fname_wsa[17:23]
short_name = tile1_fname_wsa[:23]

tile1_path_wsa = os.path.join(workspace, "AS1737/tif/{tile}/wsa/{tile1_name}".format(tile=tile, tile1_name=tile1_fname_wsa))
tile1_path_qa = os.path.join(workspace, "AS1737/tif/{tile}/qa/".format(tile=tile), tile1_fname_wsa.replace("wsa", "qa"))
tile2_path_wsa = os.path.join(workspace, "MCD43_OPS/tif/{tile}/wsa/{tile2_name}".format(tile=tile, tile2_name=tile2_fname_wsa))
tile2_path_qa = os.path.join(workspace, "MCD43_OPS/tif/{tile}/qa/".format(tile=tile), tile2_fname_wsa.replace("wsa", "qa"))


# Import tiles of interest as args > rasterio > numpy array
# For now, default to importing wsa and qa for the MCD43A3 and VNP43MA3 products
#TODO  update in future to be generic
#TODO change this to ingest hdf/h5 files, rather than converted tiffs..

tile1_ds_wsa = rio.open(tile1_path_wsa)
tile1_ds_qa = rio.open(tile1_path_qa)
tile2_ds_wsa = rio.open(tile2_path_wsa)
tile2_ds_qa = rio.open(tile2_path_qa)

tile1_band_wsa = tile1_ds_wsa.read(1)
tile1_band_qa = tile1_ds_qa.read(1)
tile2_band_wsa = tile2_ds_wsa.read(1)
tile2_band_qa = tile2_ds_qa.read(1)

# Mask the wsa values with QA to keep only value 0 (highest quality)

# Mask out nodata values
tile1_band_wsa_masked = np.ma.masked_where(tile1_band_wsa == 32767, tile1_band_wsa)
tile1_band_qa_masked = np.ma.masked_where(tile1_band_qa > 1, tile1_band_wsa_masked)
tile2_band_wsa_masked = np.ma.masked_where(tile2_band_wsa == 32767, tile2_band_wsa)
tile2_band_qa_masked = np.ma.masked_where(tile2_band_qa > 1, tile2_band_wsa_masked)


#TODO do for bsa bands as well
# bsa_swir_masked = np.ma.masked_array(bsa_band, bsa_band == 32767)
# bsa_swir_masked_qa = np.ma.masked_array(bsa_swir_masked, qa_band > 1)     

# Flaten np arrays into single column

x = tile1_band_qa_masked.flatten()
y = tile2_band_qa_masked.flatten()
cmb_data = np.column_stack((x,y))

# Calculate RMSE and Mean Bias
rmse = math.sqrt(mean_squared_error(x, y))
mb = np.sum(x - y) / x.size

# Using masked numpy arrays, create scatterplot of tile1 vs tile2
plt.ion()
fig = plt.figure()
#fig.suptitle(tile1_fname_wsa ' vs ' tile2_fname_wsa)
ax = fig.add_subplot(111)
#fig.subplots_adjust(top=0.85)

ax.set_title('White Sky Albedo Comparison')
ax.set_xlabel(tile1_fname_wsa + ' (scaled)')
ax.set_ylabel(tile2_fname_wsa + ' (scaled)')
plt.xlim(0.0, 1000)
plt.ylim(0.0, 1000)
textstr = '\n'.join((
        r'$\mathrm{RMSE}=%.2f$' % (rmse, ),
        r'$\mathrm{Mean Bias}=%.2f$' % (mb, )))

props = dict(boxstyle='round', facecolor='white', alpha=0.5)
ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
ax.plot(cmb_data[:,0], cmb_data[:,1] ,marker=',',color='b',linestyle="None")
plt_name = os.path.join(workspace, short_name) #str(year + '_' + series_name.replace(" ", ""))

# Add x=y line
lims = [
        np.min([ax.get_xlim(), ax.get_ylim()]),  # min of both axes
        np.max([ax.get_xlim(), ax.get_ylim()]),  # max of both axes
    ]

# now plot both limits against eachother
ax.plot(lims, lims, 'k-', alpha=0.75, zorder=0)
ax.set_aspect('equal')
ax.set_xlim(lims)
ax.set_ylim(lims)

print('Saving plot to: ' + '{plt_name}.png'.format(plt_name=plt_name))
plt.savefig('{plt_name}.png'.format(plt_name=plt_name))

# Make heatmap scatterplot because there are usually way too many pixels for clarity
# Uncomment the below to make a simple heatmap scatterplot. The 'bins' arg needs to be
# adjusted to make for a decent visualization.. right now everything looks like 0 density
# other than the x=y line

#heatmap, xedges, yedges = np.histogram2d(x, y, bins=50, range=[[0, 1000], [0, 1000]])
#extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
#plt.imshow(heatmap.T, extent=extent, origin='lower', cmap=cm.Reds)
#plt.savefig('{plt_name}_heatmap.png'.format(plt_name=plt_name))

# Export data as CSV in case needed
np.savetxt(short_name + 'test_data.csv', cmb_data, delimiter=",")
