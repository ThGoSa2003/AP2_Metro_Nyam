import staticmap
import sys
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from nodes import *
from constants import resolution_x, resolution_y

MetroGraph: TypeAlias = nx.Graph


def get_metro_graph() -> MetroGraph:
    """
    :returns: A graph of the metro of the city
    :warning: nodes are stored as hashable classes
    """

    stations = read_stations()
    accesses = read_accesses()

    metro_graph = MetroGraph()
    metro_graph.add_nodes_from(stations)
    metro_graph.add_nodes_from(accesses)

    for i in range(len(stations) - 1):
        if stations[i].order < stations[i + 1].order:
            metro_graph.add_edge(stations[i], stations[i + 1], type="tram",
                                 distance=distance(stations[i], stations[i+1]))
            metro_graph.add_edge(stations[i + 1], stations[i], type="tram",
                                 distance=distance(stations[i], stations[i+1]))

    stations.sort(key=lambda s: (s.name, s.line))

    for i in range(len(stations) - 1):
        if stations[i].name == stations[i + 1].name:
            metro_graph.add_edge(stations[i], stations[i + 1], type="enllaç",
                                 distance=distance(stations[i], stations[i+1]))
            metro_graph.add_edge(stations[i + 1], stations[i], type="enllaç",
                                 distance=distance(stations[i], stations[i+1]))

    stations_dict = {}
    for s in stations:
        stations_dict[s.name] = s
    for a in accesses:
        metro_graph.add_edge(a, stations_dict[a.name_station], type="acces",
                             distance=distance(a, stations_dict[a.name_station]))
        metro_graph.add_edge(stations_dict[a.name_station], a, type="acces",
                             distance=distance(a, stations_dict[a.name_station]))

    return metro_graph


def read_stations() -> Stations:
    """
    :returns: the list of stations in the city
    """

    try:
        csv_stations = pd.read_csv('./data/estacions.csv')
        dim = csv_stations.shape
        stations = []
        for i in range(dim[0]):
            id = csv_stations.iloc[i, 1]
            name = csv_stations.iloc[i, 7]
            order = csv_stations.iloc[i, 8]
            line = csv_stations.iloc[i, 11]
            pos = tuple(map(float, csv_stations.iloc[i, 26][7:-1].split()))
            stations.append(Station(id, name, order, line, pos))
        return stations
    except Exception:
        sys.exit("We cannot find data/estacions.csv, please add it in")


def read_accesses() -> Accesses:
    """
    :returns: a list of the accesses in the city
    """

    try:
        csv_accesses = pd.read_csv('./data/accessos.csv')
        dim = csv_accesses.shape
        accesses = []
        for i in range(dim[0]):
            ides = csv_accesses.iloc[i, 1]
            name = csv_accesses.iloc[i, 3]
            accessibility = csv_accesses.iloc[i, 8] == "Accessible"
            name_station = csv_accesses.iloc[i, 6]
            pos = tuple(map(float, csv_accesses.iloc[i, -1][7:-1].split()))
            accesses.append(
                Access(ides, name, accessibility, name_station, pos))
        return accesses
    except Exception:
        sys.exit("We cannot find data/accessos.csv, please add it in")


def show(g: MetroGraph) -> None:
    """
    :param g: a graph of the metro of the city
    :effect: a plot of the graph of the metro of the city will appear
    """

    positions = {}
    for n in nx.nodes(g):
        positions[n] = n.pos
    nx.draw_networkx(g, pos=positions, node_size=10, with_labels=False)
    plt.show()


def plot(g: MetroGraph, filename: str) -> None:
    """
    :param g: a graph of the metro of the city
    :param filename: a path and name to save the image
    :effect: an image of g will be saved in filename
    """

    map = staticmap.StaticMap(resolution_x, resolution_y)
    for node in g.nodes:
        map.add_marker(staticmap.CircleMarker(node.pos, "red", 10))
    for edge in g.edges:
        map.add_line(staticmap.Line([edge[0].pos, edge[1].pos], "blue", 5))
    image = map.render()
    image.save(filename)
