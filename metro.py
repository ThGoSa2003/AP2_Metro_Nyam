import networkx
import staticmap
import pandas as pd
from dataclasses import dataclass
from typing import Optional, List


MetroGraph = networkx.Graph

def get_metro_graph() -> MetroGraph:
    """

    """

    stations = read_stations()
    accessos = read_accesses()




Position = tuple[float,float]

@dataclass
class Station:
    name: str
    order: int
    line: str
    pos: Position

@dataclass
class Access:
    name: str
    accessibility: bool
    pos: Position

Stations = list[Station]

Accesses = list[Access]


def read_stations() -> Stations:
    """

    """

    csv_stations = pd.read_csv('https://raw.githubusercontent.com/jordi-petit/ap2-metro-nyam-2022/main/data/estacions.csv')
    dim = csv_stations.shape
    stations = []
    for i in range(dim[0]):
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
        name = csv_accesses.iloc[i,6]
        accessibility = csv_accesses.iloc[i,8] == "Accessible"
        pos = tuple(map(float,csv_accesses.iloc[i,-1][7:-1].split()))
        accesses.append(Access(name,accessibility,pos))
    return accesses


def show(g: MetroGraph) -> None: ...
def plot(g: MetroGraph, filename: str) -> None: ...
