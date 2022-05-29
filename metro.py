import staticmap
import sys
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing_extensions import TypeAlias
from typing import List, Tuple
from constants import resolution_x, resolution_y

Position: TypeAlias = Tuple[float, float]

MetroGraph: TypeAlias = nx.Graph

@dataclass
class Station:
    """
    This class represents a station within the metro of a city
    """

    id: int
    name: str
    order: int
    line: str
    pos: Position

    def __hash__(self) -> int:
        return hash(self.id)

@dataclass
class Access:
    """
    This class represents an access point to the metro of a city
    """

    id: int
    name: str
    accessibility: bool
    name_station: str
    pos: Position

    def __hash__(self) -> int:
        return hash(self.id)


Stations: TypeAlias = List[Station]
Accesses: TypeAlias = List[Access]

def distance(pos1: Position, pos2: Position) -> float:
    """
    :param node1, node2: any class with attribute pos (latitude and longitude)
    :returns: the euclidean distance between node1 node2
    """

    try:
        d = (pos1[0] - pos2[0])**2 + \
            (pos1[1] - pos2[1])**2
        return d**(1/2)
    except AttributeError:
        txt = "You tried to get the distance between something "
        txt += "that isn't a position."
        raise AttributeError(txt)
        sys.exit()

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
            d = distance(stations[i].pos, stations[i+1].pos)
            metro_graph.add_edge(stations[i], stations[i + 1], type="tram",
                                 distance=d)
            metro_graph.add_edge(stations[i + 1], stations[i], type="tram",
                                 distance=d)

    stations.sort(key=lambda s: (s.name, s.line))

    for i in range(len(stations) - 1):
        if stations[i].name == stations[i + 1].name:
            d = distance(stations[i].pos, stations[i+1].pos)
            metro_graph.add_edge(stations[i], stations[i + 1], type="enllaç",
                                 distance=d)
            metro_graph.add_edge(stations[i + 1], stations[i], type="enllaç",
                                 distance=d)

    stations_dict = {}
    for s in stations:
        stations_dict[s.name] = s
    for a in accesses:
        d = distance(a.pos, stations_dict[a.name_station].pos)
        metro_graph.add_edge(a, stations_dict[a.name_station], type="acces",
                             distance=d)
        metro_graph.add_edge(stations_dict[a.name_station], a, type="acces",
                             distance=d)

    return metro_graph


def read_stations() -> Stations:
    """
    :returns: the list of stations in the city
    """

    try:
        csv_stations = pd.read_csv('./estacions.csv')
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
        csv_accesses = pd.read_csv('./accessos.csv')
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

    metro_map = staticmap.StaticMap(resolution_x, resolution_y)
    for node in g.nodes:
        metro_map.add_marker(staticmap.CircleMarker(node.pos, "red", 10))
    for edge in g.edges:
        metro_map.add_line(staticmap.Line([edge[0].pos, edge[1].pos],
                                          "blue", 5))
    image = metro_map.render()
    image.save(filename)
