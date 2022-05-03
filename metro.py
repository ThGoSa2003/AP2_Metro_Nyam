import networkx as nx
import staticmap
import pandas as pd
from dataclasses import dataclass
from typing import Optional, List, Tuple
import matplotlib.pyplot as plt

Position = Tuple[float,float]

@dataclass
class Station:
    id_station: int
    name: str
    order: int
    line: str
    pos: Position

    def __hash__(self):
        return hash(self.id_station)

@dataclass
class Access:
    id_access: int
    name: str
    accessibility: bool
    name_station: str
    pos: Position

    def __hash__(self):
        return hash(self.id_access)

Stations = List[Station]

Accesses = List[Access]

MetroGraph = nx.Graph

def get_metro_graph() -> MetroGraph:
    """

    """
    def distance(station1: Optional[Station], station2: Optional[Station]) -> float:
        return ((station1.pos[0] - station2.pos[0])**2 + (station1.pos[1] - station2.pos[1])**2)**1/2

    stations = read_stations()
    accesses = read_accesses()
    metro_graph = MetroGraph()
    metro_graph.add_nodes_from(stations)
    metro_graph.add_nodes_from(accesses)
    for i in range(len(stations) - 1):
        if stations[i].order < stations[i + 1].order:
            metro_graph.add_edge(stations[i], stations[i + 1], type = "tram", distance = distance(stations[i],stations[i+1]))
            metro_graph.add_edge(stations[i + 1], stations[i], type = "tram", distance = distance(stations[i],stations[i+1]))
    stations.sort(key = lambda s : (s.name,s.line))
    for i in range(len(stations) - 1):
        if stations[i].name == stations[i + 1].name:
            metro_graph.add_edge(stations[i], stations[i + 1], type = "enllaç",distance = distance(stations[i],stations[i+1]))
            metro_graph.add_edge(stations[i + 1], stations[i], type = "enllaç",distance = distance(stations[i],stations[i+1]))
    stations_dict = {}
    for s in stations:
        stations_dict[s.name] = s
    for a in accesses:
        metro_graph.add_edge(a, stations_dict[a.name_station], type = "acces", distance = distance(a,stations_dict[a.name_station]))
        metro_graph.add_edge(stations_dict[a.name_station], a, type = "acces", distance = distance(a,stations_dict[a.name_station]))
    return metro_graph

def read_stations() -> Stations:
    """

    """

    csv_stations = pd.read_csv('https://raw.githubusercontent.com/jordi-petit/ap2-metro-nyam-2022/main/data/estacions.csv')
    dim = csv_stations.shape
    stations = []
    for i in range(dim[0]):
        id_station = csv_stations.iloc[i, 5]
        name = csv_stations.iloc[i,7]
        order = csv_stations.iloc[i,8]
        line = csv_stations.iloc[i,11]
        pos = tuple(map(float,csv_stations.iloc[i,26][7:-1].split()))
        stations.append(Station(id_station,name,order,line,pos))
    return stations

def read_accesses() -> Accesses:
    """

    """

    csv_accesses = pd.read_csv('https://raw.githubusercontent.com/jordi-petit/ap2-metro-nyam-2022/main/data/accessos.csv')
    dim = csv_accesses.shape
    accesses = []
    for i in range(dim[0]):
        id_accesses = csv_accesses.iloc[i, 1]
        name = csv_accesses.iloc[i,3]
        accessibility = csv_accesses.iloc[i,8] == "Accessible"
        name_station = csv_accesses.iloc[i,6]
        pos = tuple(map(float,csv_accesses.iloc[i,-1][7:-1].split()))
        accesses.append(Access(id_accesses, name,accessibility,name_station,pos))
    return accesses


def show(g: MetroGraph) -> None:
    positions = {}
    for n in  nx.nodes(g):
        positions[n] = n.pos
    nx.draw_networkx(g,pos = positions, node_size = 10, with_labels = False)
    plt.show()

def plot(g: MetroGraph, filename: str) -> None:
    positions = {}
    for n in  nx.nodes(g):
        positions[n] = n.pos
    nx.draw_networkx(g,pos = positions, node_size = 10, with_labels = False)
    plt.savefig(filename + ".png")
