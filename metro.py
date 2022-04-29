import networkx as nx
import staticmap
import pandas as pd
from dataclasses import dataclass
from typing import Optional, List


MetroGraph = nx.Graph

def get_metro_graph() -> MetroGraph:
    """

    """

    stations = read_stations()
    accesses = read_accesses()
    metro_graph = MetroGraph()
    metro_graph.add_nodes_from(stations)
    metro_graph.add_nodes_from(accesses)
    for i in range(len(stations) - 1):
        if stations[i].order


Position = tuple[float,float]

@dataclass
class Station:
    id_station: int
    name: str
    order: int
    line: str
    pos: Position

    def __hash__():
        return hash(id_station)

@dataclass
class Access:
    id_access: int
    name: str
    accessibility: bool
    name_station: str
    pos: Position

    def __hash__():
        return hash(id_access)

Stations = list[Station]

Accesses = list[Access]


def read_stations() -> Stations:
    """

    """

    csv_stations = pd.read_csv('https://raw.githubusercontent.com/jordi-petit/ap2-metro-nyam-2022/main/data/estacions.csv')
    dim = csv_stations.shape
    stations = []
    for i in range(dim[0]):
        id_station = csv_stations.iloc[i, 5]
        name = csv_stations.iloc[i,7]
        order = csv_stations.iloc[i,9]
        line = csv_stations.iloc[i,12]
        pos = tuple(map(float,csv_stations.iloc[i,26][7:-1].split()))
        stations.append(Station(name,order,line,pos))
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
        accesses.append(Access(name,accessibility,name_station,pos))
    return accesses


def show(g: MetroGraph) -> None: ...
def plot(g: MetroGraph, filename: str) -> None: ...
