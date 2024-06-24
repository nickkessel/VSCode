from mpl_toolkits.basemap import Basemap
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import csv

lats, lons, names, alt = [], [],[],[]

with open('C:/Users/nickk/Documents/VSCode/maps/asos_stations.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter= ',')
    for data in reader:
        if float(data['UTC'])>-5. or float(data['UTC'])<-8. or float(data['ELEV'])<0.0:
            continue
        names.append(data['CALL'])
        lats.append(float(data['LAT']))
        lons.append(float(data['LON']))
        alt.append(float(data['ELEV']))
        
#how much to zoom from coords (in deg)
scale = 0

bbox = [np.min(lats) - scale, np.max(lats) + scale, \
    np.min(lons) - scale, np.max(lons) + scale]

fig, ax = plt.subplots(figsize=(12,8))

m = Basemap(projection='merc',llcrnrlat=bbox[0],urcrnrlat=bbox[1],\
            llcrnrlon=bbox[2],urcrnrlon=bbox[3],lat_ts=10,resolution='i')

m.drawcoastlines()
m.drawstates()
m.drawcountries()
m.drawrivers(linewidth=.35, color = '#2233CC')
m.fillcontinents(color = '#88CC88', lake_color = 'dodgerblue')

m.drawparallels(np.arange(bbox[0],bbox[1],(bbox[1]-bbox[0])/5),labels=[1,0,0,0])
m.drawmeridians(np.arange(bbox[2],bbox[3],(bbox[3]-bbox[2])/5),labels=[0,0,0,1],rotation=45)
m.drawmapboundary(fill_color='dodgerblue')

alt_min = np.min(alt)
alt_max = np.max(alt)
cmap = plt.get_cmap('gist_earth')
normalize = matplotlib.colors.Normalize(vmin=alt_min, vmax = alt_max)

for ii in range(0, len(alt)):
    x,y = m(lons[ii],lats[ii])
    name = names[ii]
    color_interp = np.interp(alt[ii], [alt_min, alt_max], [10,250])
    m.plot(x,y, 'o', markersize =5, color = cmap(int(color_interp)))
    plt.text(x + 1,y + 1, name)
    

plt.title("ASOS Station Distribution")
cax, _ = matplotlib.colorbar.make_axes(ax)
cbar = matplotlib.colorbar.ColorbarBase(cax, cmap=cmap,norm=normalize,label='Elevation')

plt.show()