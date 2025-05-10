import osmnx as ox
import matplotlib.pyplot as plt

address = '139 Cleveland Ave milford oh 45150'
G = ox.graph_from_address(address, retain_all = True, dist = 1000, dist_type= 'bbox', network_type='drive')

# assign colors to edges based on "highway" value
hwy_color = {'residential': 'gray', 
             'trunk': 'white',
             'trunk_link': 'white',
             'secondary': 'yellow',
             'secondary_link': 'darkkhaki',
             'tertiary': 'green',
             'tertiary_link': 'darkgreen',
             'primary': 'orange',
             'primary_link': 'darkorange',
                 
             'motorway': 'red',
             'motorway_link' : 'brown',
             'unclassified': 'lightgreen',
             'living_street' : 'brown'}
edges = ox.graph_to_gdfs(G, nodes=False)['highway']
ec = edges.replace(hwy_color)

# plot graph using these colors
fig = ox.plot_graph(G, node_size = 0, edge_color=ec, save = True, 
 filepath = 'C:/Users/nickk/Documents/VSCode/maps/produced/cinti6.jpg', dpi = 500)


