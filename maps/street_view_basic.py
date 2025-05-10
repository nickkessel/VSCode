import osmnx as ox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

place = ['milford, ohio']
target_address = ('139 Cleveland ave milford oh 45150')
gdf_nodes = gdf_edges = None
for place in place:
    G = ox.graph_from_address(target_address, dist = 5500, dist_type= 'bbox', retain_all = True, simplify = False, network_type= 'drive')
    n_, e_ = ox.graph_to_gdfs(G)
    n_["place"] = place
    e_["place"] = place
    if gdf_nodes is None:
        gdf_nodes = n_
        gdf_edges = e_
    else:
        gdf_nodes = pd.concat([gdf_nodes, n_])
        gdf_edges = pd.concat([gdf_edges, e_])
road_color = {
    'residential': 'gray',
    'secondary': 'r',
    'tertiary': 'y',
    'unclassified': 'b'
}
fig = gdf_edges.plot(column="place", figsize = (10,10),
                     alpha = 1, linewidth = 1, edgecolor = 'red')

#plt.suptitle("test")
fig.set_facecolor('black')
plt.title("Milford Roadways")
plt.xticks([])
plt.yticks([])
plt.savefig("milford11.jpg", dpi=600, format="jpg")
plt.show()