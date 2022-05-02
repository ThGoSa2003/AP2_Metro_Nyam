import networkx as nx
import staticmap
import pandas as pd
from dataclasses import dataclass
from typing import Optional, List
import matplotlib.pyplot as plt

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


MetroGraph = nx.Graph

def by_name(station1: Station, station2: Station) -> bool:

    if station1.name < station2.name:
        return True
    if station2.name > station2.name:
        return False
    if station1.line < station2.line:
        return True
    return False

def by_station_name(access1: Access, access2: Access) -> bool:

    if access1.station_name < access2.station_name:
        return True
    if access2.station_name > access2.station_name:
        return False
    if access1.name < access2.name:
        return True
    return False

def get_metro_graph() -> MetroGraph:
    """

    """

    stations = read_stations()
    accesses = read_accesses()
    metro_graph = MetroGraph()
    metro_graph.add_nodes_from(stations)
    metro_graph.add_nodes_from(accesses)
    for i in range(len(stations) - 1):
        if stations[i].order < station[i + 1].order:
            metro_graph.add_edge(stations[i], stations[i + 1], type = "tram")
            metro_graph.add_edge(stations[i + 1], stations[i], type = "tram")
    sort(stations, key=by_name)
    for i in range(len(stations) - 1):
        if stations[i].name == station[i + 1].name:
            metro_graph.add_edge(stations[i], stations[i + 1], type = "transbord")
            metro_graph.add_edge(stations[i + 1], stations[i], type = "transbord")
    sort(accesses, key=by_station_name)
    access_idx = 0
    for station in stations:
        while accesses[access_idx].station_name == station.name:
            metro_graph.add_edge(station, access[access_idx], type = "transbord")
            metro_graph.add_edge(access[access_idx], station, type = "transbord")
            access_idx += 1
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


def show(g: MetroGraph) -> None:...

    g = nx.Graph()

    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(1, 4)
    g.add_edge(1, 5)
    plt.figure()
    nx.draw(g, with_labels = True)
    plt.show()

def plot(g: MetroGraph, filename: str) -> None: ...
