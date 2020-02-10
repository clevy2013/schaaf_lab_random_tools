#!/home/arthur.elmes/software/anaconda3/envs/geo/bin/python

import os, matplotlib, math, sys
import matplotlib.pyplot as plt
#from matplotlib import cm
from sklearn.metrics import mean_squared_error
import numpy as np
#import pandas as pd
#import rasterio as rio
from pyhdf.SD import SD, SDC
import h5py

matplotlib.rcParams['agg.path.chunksize'] = 100000

## h12v04 UL: -6671703.1179999997839332 5559752.5983330002054572 LR: -5559752.5983330002054572 4447802.0786669999361038
## h16v01 UL: -2223901.0393329998478293 8895604.1573329996317625 LR: -1111950.5196670000441372 7783653.6376670002937317
## h16v02 UL: -2223901.0393329998478293 7783653.6376670002937317 LR: -1111950.5196670000441372 6671703.1179999997839332

def modis_process():
    #TODO fill in the processing chain for modis hdf products here, calling hdf_to_np etc
    pass

def viirs_process():
    #TODO mirror the modis processing chain that's already laid out and working, but with h5py
    pass

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
    fig.suptitle(labels[0] + '_' + labels[1])
    ax = fig.add_subplot(111)
    #fig.subplots_adjust(top=0.85)

    ax.set_title(labels[3])
    ax.set_xlabel(labels[1] + " " + labels[4] + ' (scaled)')
    ax.set_ylabel(labels[2] + " " + labels[5] + ' (scaled)')
    plt.xlim(0.0, 1000)
    plt.ylim(0.0, 1000)

    # Add text box with RMSE and mean bias
    textstr = '\n'.join((
        r'$\mathrm{RMSE}=%.2f$' % (stats[0], ),
        r'$\mathrm{Mean Bias}=%.2f$' % (stats[1], )))

    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
    ax.plot(cmb_data[:, 0], cmb_data[:, 1], marker=',', color='b', linestyle="None")
    #TODO add band name to this plot output name
    plt_name = os.path.join(workspace, labels[0] + "_" + labels[1] + "_" + labels[4] + "_vs_" \
                            + labels[2] + "_" + labels[5])

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
    hdrs = str(labels[1] + "." + labels[4] + "," + labels[2] + "." + labels[5])
    np.savetxt(labels[0] + "_" + labels[1] + "_" + labels[2] + '_test_data.csv', cmb_data, delimiter=",", header=hdrs)

def main():
    # Set workspace IO dirs
    workspace = sys.argv[1] #"/muddy/data05/arthur.elmes/MCD43/MCD43A3/h12v04/"
    workspace_out = workspace 
    os.chdir(workspace)

    # test tile 1 filename: MCD43A3.A2016365.h12v04.006.2017014043109.hdf
    # test tile 2 filename: MCD43A3.A2016366.h12v04.006.2017014050856.hdf 
    
    #TODO these shouldn't just be wsa, should be able to do
    # any band, selected as argument they should be args so
    # that different bands can be selected. Right now these are manually set
    # to reflect the band of interest
    
    # sds_name_wsa = "Albedo_WSA_shortwave"
    # sds_name_qa = "BRDF_Albedo_Band_Mandatory_Quality_shortwave"
    sds_name_wsa = "Albedo_WSA_nir"
    sds_name_qa = "BRDF_Albedo_Band_Mandatory_Quality_nir"
    
    # Set input hdf/h5 filenames
    #TODO replace hard coded with cl args
    tile1_fname =  sys.argv[2] #TODO maybe later add an os.path.join with the workspace here? but maybe not
    tile2_fname =  sys.argv[3]

    # Extract identifying information from filenames
    sensor = tile1_fname.split("/")[-1][:3]
    
    # Check that sensor is sensible
    if ( sensor == "MCD" ):
        tile = tile1_fname.split("/")[-1][17:23]
        short_name_tile1 = tile1_fname.split("/")[-1][:16]
        short_name_tile2 = tile2_fname.split("/")[-1][:16]
        collection_tile1 = tile1_fname.split("/")[-1][24:27]
        collection_tile2 = tile2_fname.split("/")[-1][24:27]
    elif ( sensor == "VNP" ):
        tile = tile1_fname.split("/")[-1][18:24]
        short_name_tile1 = tile1_fname.split("/")[-1][:17]
        short_name_tile2 = tile2_fname.split("/")[-1][:17]
        collection_tile1 = tile1_fname.split("/")[-1][25:28]
        collection_tile2 = tile2_fname.split("/")[-1][25:28]
    elif ( sensor != "MCD" and sensor != "VNP"):
        print("Check input data type!")
        sys.exit()

    labels = (tile, short_name_tile1, short_name_tile2, sds_name_wsa, collection_tile1, collection_tile2)

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
