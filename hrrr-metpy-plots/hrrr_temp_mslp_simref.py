#-------TODOS:-------
#option to toggle absolute (pivotal-like scale for temps) or relative colormap
#going off #1 here... custom temps colortable
#option to set forecast hour

#super cool imports
from datetime import datetime, timedelta, date, timezone
from siphon.catalog import TDSCatalog 
import xarray as xr
import numpy as np
import metpy.calc as mpcalc
import metpy.units as units

from metpy.plots.declarative import (BarbPlot, ContourPlot, FilledContourPlot, MapPanel,
                                     PanelContainer, PlotObs)
#access hrrr data from ucar server, open as xarray
best_hrrr = TDSCatalog("https://thredds.ucar.edu/thredds/catalog/grib/NCEP/HRRR/CONUS_2p5km/catalog.html?dataset=grib/NCEP/HRRR/CONUS_2p5km/Best")
best_ds= best_hrrr.datasets[0]
ds=xr.open_dataset(best_ds.access_urls['OPENDAP'])

cbar_style = 0

#this gets current time, and will pull the most recent model output 
now =  datetime.now(timezone.utc) 
current_time = str(now.strftime('%Y-%m-%d')) + 'T' + str(now.strftime("%H")) #string to give to model
print('time: ' + current_time)

#-----spatial domains----- FORMAT: (x1, x2, y1, y2, name)
domain_midwest = [-200, 2000, 1200, 2700, 'midwest'] #Minnesota to Virginia
domain_michigan = [100, 1200, 1800, 2600, 'michigan'] #michigan and wisconsin 
domain_conus = [-2650, 2300, 0, 3000, 'conus'] #conus, might take a while to load 
domain_mountain_west = [-2400, -500, 1000, 2900, 'mountain west'] #washington state to new mexico
domain_appalachia = [600, 2100, 1000, 2400, 'appalachia'] #northern alabama to vermont
domain_ohio = [800, 1350, 1550, 2000, 'ohio'] #its just ohio
domain_cincinnati = [875, 975, 1600, 1660, 'cincinnati'] #silly over-zoomed in view of sw ohio

# Map user-friendly names to domain variables
domain_options = {
    'midwest': domain_midwest,
    'michigan': domain_michigan,
    'conus': domain_conus,
    'mountain_west': domain_mountain_west,
    'appalachia': domain_appalachia,
    'ohio': domain_ohio,
    'cincinnati': domain_cincinnati
}

user_domain = input("Choose domain (midwest, michigan, conus, mountain_west, appalachia, ohio, cincinnati): ").strip().lower()

if user_domain not in domain_options:
    raise ValueError(f"Invalid domain name: {user_domain}")

target_domain = domain_options[user_domain]

user_cbar_style = input("relative (r) or absolute (a) colorbar: ").strip().lower()

if user_cbar_style == 'r':
    cbar_style = 0
elif user_cbar_style == 'a':
    cbar_style = 1
else:
    raise ValueError(f'error! do not recognize string: {user_cbar_style}. Enter r or a')
    

#these are the only vars we are pulling, to expedite the file opening process 
using_vars = ['LambertConformal_Projection', 'Composite_reflectivity_entire_atmosphere', 'Pressure_reduced_to_MSL_msl', 'Temperature_height_above_ground']
ds_preprocess = ds[using_vars] #only the useful variables are being selected

print("min x:", ds_preprocess.x.values.min(), "to max:", ds_preprocess.x.values.max()) #see what x,y coords the model's bounds are
print("min y:", ds_preprocess.y.values.min(), "to max:", ds_preprocess.y.values.max())
#slice ds to remove unneccesary timestamps and only select midwest data
ds_preprocess = ds_preprocess.metpy.sel(x=slice(target_domain[0], target_domain[1]), y=slice(target_domain[2], target_domain[3]), time=slice(current_time, current_time))

#parse dataset, which will be much faster bc we are only doing 1 timestamp/5 products/ 1/4 the size map
ds_domain = ds_preprocess.metpy.parse_cf()
ds_domain['msl_mb']= ds_domain['Pressure_reduced_to_MSL_msl'].metpy.convert_units('hPa')
ds_domain['temp_f'] = ds_domain['Temperature_height_above_ground'].metpy.convert_units('degF')
plot_time = datetime(now.year, now.month, now.day, now.hour) #set product time

colorbar_bin_width = 5 #width of each bin in the colorbar

#experimenting with a log scale colortable except i'm not actually using it rn
contours = np.unique(np.round(np.logspace(0, 2, 20) - 1))  # e.g., 0 to 99
contours = contours[contours <= 100]  # Ensure max is 100

#create a filled contour plot from high cloud data
composite_ref = FilledContourPlot()
composite_ref.data = ds_domain #dataset we're using
composite_ref.field = 'Composite_reflectivity_entire_atmosphere' #var we're plotting
composite_ref.level = None #no pressure/altitude level
composite_ref.time = plot_time 
composite_ref.contours = np.arange(0,81,colorbar_bin_width).tolist() #0 to 101 (exclusive) with intervals every colorbar_bin_width
composite_ref.colormap = 'NWSReflectivity' #using predefined matplot 'Blues' cmap, reversed so blue = no cloud
composite_ref.colorbar = {
    'orientation': 'horizontal',
    'shrink': 0.7, 'pad': 0.01, 'aspect': 40.0
}
composite_ref.plot_units = 'dB'
#composite_ref.mpl_args = 

#temps
param2 = FilledContourPlot()
param2.data = ds_domain #dataset we're using
param2.field = 'temp_f' #var we're plotting
param2.level = None #no pressure/altitude level
param2.time = plot_time 
if cbar_style == 0:
    param2.contours = np.arange(round((ds_domain.temp_f.values.min() - 1), 1), round((ds_domain.temp_f.values.max() + 1), 1) ,0.1).tolist()
    param2.colormap = 'seismic' 
elif cbar_style == 1:
    param2.contours = np.arange(0,101,5).tolist()
    param2.colormap = 'turbo' 

param2.colorbar = {
    'orientation': 'horizontal',
    'shrink': 0.7,
    'pad': -0.05# Shrinks the colorbar to 70% of default length
}
param2.plot_units = 'degF'
param2.clabels = True

#mslp
param3 = ContourPlot()
param3.data = ds_domain #dataset we're using
param3.field = 'msl_mb' #var we're plotting
param3.level = None #no pressure/altitude level
param3.time = plot_time 
param3.contours = np.arange(ds_domain.msl_mb.values.min(),ds_domain.msl_mb.values.max(),2).tolist() #0 to 101 (exclusive) with intervals every colorbar_bin_width
param3.plot_units = 'hPa'
param3.clabels = True

panel1 = MapPanel() #create map panel
panel1.area = None #I'm letting the x,y coords built into the hrrr output dictate the scope of the map NOT lat/lon
panel1.projection = ds_domain['Composite_reflectivity_entire_atmosphere'].metpy.cartopy_crs #use projection from model output
panel1.layers = ['states', 'coastline', 'borders'] #what we want on the map
panel1.title = f'HRRR CompositeRef, mslp, surface temps at {plot_time} [{target_domain[4]}]' #set title
panel1.plots = [param2, composite_ref, param3] #choose plots

panel1.layout = (1,1,1) #(row, column, position) in the final panel container

print('Min Temp: ', ds_domain.temp_f.values.min(), ' Max Temp: ', ds_domain.temp_f.values.max(),
      '\nMin MSLP: ', ds_domain.msl_mb.values.min(), ' Max MSLP: ', ds_domain.msl_mb.values.max(),
     '\nMin ref: ', ds_domain.Composite_reflectivity_entire_atmosphere.values.min(), ' Max ref: ', ds_domain.Composite_reflectivity_entire_atmosphere.values.max())

pc = PanelContainer() #create panel container

ratio_x = (target_domain[1] - target_domain[0]) / (target_domain[3] - target_domain[2])
print(ratio_x)

pc.size = (12 * ratio_x, 12) #dynamically set size of pc based on aspect ratio of domain
pc.panels = [panel1] #all panels we want in the pc
pc.save('test.png', dpi = 200)
pc.show()
