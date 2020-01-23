#!/home/arthur.elmes/software/anaconda3/envs/geo/bin/python

import os, glob, matplotlib, math, sys
import matplotlib.pyplot as plt
from matplotlib import cm
from sklearn.metrics import mean_squared_error
import numpy as np
import pandas as pd
import rasterio as rio
from pyhdf.SD import SD, SDC 

matplotlib.rcParams['agg.path.chunksize'] = 100000

def hdf_to_np(hdf_fname, sds):
    hdf_ds = SD(hdf_fname, SDC.READ)
    dataset_3d = hdf_ds.select(sds)
    data_np = dataset_3d[:,:]
    return data_np

def mask_qa(hdf_data, hdf_qa):
    # Mask the wsa values with QA to keep only value 0 (highest quality)
    # Also, mask out nodata values (32767)
    nodata_masked = np.ma.masked_where(hdf_data == 32767, hdf_data)
    qa_masked = np.ma.masked_where(hdf_qa > 1, nodata_masked)
    return qa_masked

def plot_data(cmb_data, labels, stats, workspace):
    # Using masked numpy arrays, create scatterplot of tile1 vs tile2
    plt.ion()
    fig = plt.figure()
    fig.suptitle(labels[1] + ' vs ' + labels[2])
    ax = fig.add_subplot(111)
    #fig.subplots_adjust(top=0.85)

    ax.set_title('White Sky Albedo Comparison')
    ax.set_xlabel(labels[1] + ' (scaled)')
    ax.set_ylabel(labels[2] + ' (scaled)')
    plt.xlim(0.0, 1000)
    plt.ylim(0.0, 1000)

    # Add text box with RMSE and mean bias
    textstr = '\n'.join((
        r'$\mathrm{RMSE}=%.2f$' % (stats[0], ),
        r'$\mathrm{Mean Bias}=%.2f$' % (stats[1], )))

    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
    ax.plot(cmb_data[:, 0], cmb_data[:, 1], marker=',', color='b', linestyle="None")
    plt_name = os.path.join(workspace, labels[0]) #str(year + '_' + series_name.replace(" ", ""))

    # Add x=y line
    lims = [
        np.min([ax.get_xlim(), ax.get_ylim()]),  # min of both axes
        np.max([ax.get_xlim(), ax.get_ylim()]),  # max of both axes
    ]

    # Plot limits against each other for 1:1 line
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
    np.savetxt(labels[1] + "_" + labels[2] + 'test_data.csv', cmb_data, delimiter=",")

def main():
    # Set workspace IO dirs
    workspace = "/muddy/data05/arthur.elmes/MCD43/MCD43A3/h12v04/"
    # workspace = sys.argv[1]

    os.chdir(workspace)

    # tile1_fname_wsa = sys.argv[2]
    # tile2_fname_wsa = sys.argv[3]

    # These probably won't ever change, but maybe they should be args so
    # that different bands can be selected
    sds_name_wsa = "Albedo_WSA_shortwave"
    sds_name_qa = "BRDF_Albedo_Band_Mandatory_Quality_shortwave"

    # Set input hdf/h5 filenames
    #TODO replace hard coded with cl args
    tile1_fname = os.path.join(workspace,"MCD43A3.A2016366.h12v04.006.2017014050856.hdf")
    tile2_fname = os.path.join(workspace, "MCD43A3.A2016365.h12v04.006.2017014043109.hdf")

    # Extract identifying information from filenames
    tile = tile1_fname.split("/")[-1][17:23]
    short_name_tile1 = tile1_fname.split("/")[-1][:16]
    short_name_tile2 = tile2_fname.split("/")[-1][:16]
    labels = (tile, short_name_tile1, short_name_tile2)
    
    # Convert both tiles' data and qa to numpy arrays for plotting
    tile1_data_wsa = hdf_to_np(tile1_fname, sds_name_wsa)
    tile2_data_wsa = hdf_to_np(tile2_fname, sds_name_wsa)
    tile1_data_qa = hdf_to_np(tile1_fname, sds_name_qa)
    tile2_data_qa = hdf_to_np(tile2_fname, sds_name_qa)

    # Call masking function to cleanup data
    tile1_data_qa_masked = mask_qa(tile1_data_wsa, tile1_data_qa)
    tile2_data_qa_masked = mask_qa(tile2_data_wsa, tile2_data_qa)
    # print(tile1_data_qa_masked)
    # print(tile1_data_qa)
    # Flaten np arrays into single column
    x = tile1_data_qa_masked.flatten()
    y = tile2_data_qa_masked.flatten()
    cmb_data = np.column_stack((x,y))

    # Calculate RMSE and Mean Bias, multiply by 0.001, which is the scale factor for MCD43/VNP43
    rmse = math.sqrt(mean_squared_error(x, y)) * 0.001
    mb = np.sum(x - y) / x.size * 0.001
    stats = (rmse, mb)
    
    # Call plotting function
    plot_data(cmb_data, labels, stats, workspace)
    
if __name__ == "__main__":
    main()
