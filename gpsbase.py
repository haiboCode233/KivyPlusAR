import osmnx as ox

G = ox.graph_from_place('Shanghai, China')
ox.plot_graph(G, save=True, filepath='./map.png')