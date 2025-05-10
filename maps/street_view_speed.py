import osmnx as ox
import matplotlib.pyplot as plt

address = '1-1 Chiyoda, Chiyoda City, Tokyo 100-8111, Japan'
point = [35.683270,139.766796]

G = ox.graph_from_point(point, retain_all = True, simplify = False, dist = 12500, dist_type= 'bbox', network_type='drive')
G = ox.add_edge_speeds(G)

ec = ox.plot.get_edge_colors_by_attr(G, 'speed_kph', cmap = 'viridis')

# plot graph using these colors
fig = ox.plot_graph(G, node_size = 0, edge_color=ec, save = True, 
 filepath = 'C:/Users/nickk/Documents/VSCode/maps/produced/tokyo1.jpg', dpi = 600)


