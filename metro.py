import networkx
import staticmap
import pandas as pd
from dataclasses import dataclass
from typing import Optional, List


MetroGraph = networkx.Graph

def get_metro_graph() -> MetroGraph: ...


Position = tuple[float,float]

@dataclass
class Station:
    name: str
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
    csv_estacions = pd.read_csv('https://raw.githubusercontent.com/jordi-petit/ap2-metro-nyam-2022/main/data/estacions.csv')
    dim = csv_estacions.shape
    stations = []
    for i in range(dim[0]):
        name = csv_estacions.iloc[i,7]
        accessibility = csv_estacions.iloc[i,18] == "Accessible"
        pos = tuple(map(float,csv_estacions.iloc[i,26][7:-1].split()))
        stations.append(Station(name,accessibility,pos))
    return stations

def read_accesses() -> Accesses:

    csv_accessos = pd.read_csv('https://raw.githubusercontent.com/jordi-petit/ap2-metro-nyam-2022/main/data/blob/main/accessos.csv')
    dim = csv_accessos.shape
    accessos = []
    for i in range(dim[0]):
        name = csv_accessos.iloc[i,6]
        accessibility = csv_accessos.iloc[i,8] == "Accessible"
        pos = 
        accessos.append(Restaurant(name, accessibility))
    return accessos


def show(g: MetroGraph) -> None: ...
def plot(g: MetroGraph, filename: str) -> None: ...
