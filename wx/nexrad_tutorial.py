import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.dates as mdates

import cartopy.crs as ccrs
import pyart
import pandas as pd

import nexradaws
import tempfile
import pytz

templocation = tempfile.mkdtemp()

import cartopy.feature as cfeature
from metpy.plots import USCOUNTIES

radar_id = 'KDVN'
start = pd.Timestamp(2020,8,10,16,30).tz_localize(tz='UTC')
end = pd.Timestamp(2020,8,10,21,30).tz_localize(tz='UTC')

#map bounds
min_lon = -93.25
max_lon = -88
min_lat = 40.35
max_lat = 43.35

#get data
conn = nexradaws.NexradAwsInterface()
scans = conn.get_avail_scans_in_range(start, end, radar_id)
print("there are {} scans between {} and {} \n".format(len(scans), start,end))
print(scans[0:4])

#download scans (just 2 so it doesnt take too long)
results = conn.download(scans[0:2], templocation)

##loop thru radar images
for i, scan in enumerate(results.iter_success(), start=1):
    
    if scan.filename[-3:] != "MDM": #no files ending in MDM
        print(str(i))
        print("working on "+scan.filename)
        
        this_time = pd.to_datetime(scan.filename[4:17], format = "%Y%m%d_%H%M").tz_localize("UTC")
        
        radar = scan.open_pyart()
        
        fig = plt.figure()
        
        map_panel_axes = [0.05, 0.05, .4, .80]
        x_cut_panel_axes = [0.55, 0.10, .4, .25]
        y_cut_panel_axes = [0.55, 0.50, .4, .25]

        projection = ccrs.PlateCarree() 
        
        #apply filter to cut off low reflectiveity vals
        
        gatefilter = pyart.filters.GateFilter(radar)
        
        gatefilter.exclude_below('reflectivity', -2)
        
        display = pyart.graph.RadarMapDisplay(radar)
        
        ax1 = fig.add_axes(map_panel_axes, projection=projection)
        ax1.add_feature(USCOUNTIES.with_scale('500k'), edgecolor="gray", linewidth=0.4)
        ax1.add_feature(cfeature.STATES.with_scale('10m'), linewidth=1.0)
        
        cf = display.plot_ppi_map('reflectivity', 0, vmin=-7.5, vmax=65,
                    min_lon=min_lon, max_lon=max_lon, min_lat=min_lat, max_lat=max_lat,
                    title=radar_id+" reflectivity and severe weather reports, "+this_time.strftime("%H%M UTC %d %b %Y"),
                    projection=projection, resolution='10m',
                        gatefilter=gatefilter,
                    cmap='pyart_HomeyerRainbow', 
                    colorbar_flag=False,
                    lat_lines=[0,0], lon_lines=[0,0]) ## turns off lat/lon grid lines
        #display.plot_crosshairs(lon=lon, lat=lat)
        
        ## plot horizontal colorbar 
        display.plot_colorbar(cf,orient='horizontal', pad=0.07)
        
        # Plot range rings if desired
        #display.plot_range_ring(25., color='gray', linestyle='dashed')
        #display.plot_range_ring(50., color='gray', linestyle='dashed')
        #display.plot_range_ring(100., color='gray', linestyle='dashed')

        ax1.set_xticks(np.arange(min_lon, max_lon, .5), crs=ccrs.PlateCarree())
        ax1.set_yticks(np.arange(min_lat, max_lat, .5), crs=ccrs.PlateCarree())     
       

        plt.savefig(scan.radar_id+"_"+scan.filename[4:17]+"_dz_rpts.png",bbox_inches='tight',dpi=300,
                   facecolor='white', transparent=False)
        #plt.show()
        plt.close('all')
        
        