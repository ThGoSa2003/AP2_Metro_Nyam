import networkx
import osmnx as ox
import haversine
import pandas
import pandas as pd
import staticmap
from metro import *


url = 'https://raw.githubusercontent.com/jordi-petit/ap2-metro-nyam-2022/main/data/restaurants.csv'
csv_restaurants = pd.read_csv(url)
url = 'https://raw.githubusercontent.com/jordi-petit/ap2-metro-nyam-2022/main/data/blob/main/estacions.csv'
csv_restaurants = pd.read_csv(url)
url = 'https://raw.githubusercontent.com/jordi-petit/ap2-metro-nyam-2022/main/data/blob/main/accessos.csv'
csv_restaurants = pd.read_csv(url)


CityGraph = networkx.Graph
OsmnxGraph = networkx.MultiDiGraph


def get_osmnx_graph() -> OsmnxGraph:
    return ox.graph_from_place("Barcelona, Spain", network_type = "walk")


def save_osmnx_graph(g: OsmnxGraph, filename: str) -> None:
    ox.save_load.save_graph_osm(g, filename=filename+".osm")
def load_osmnx_graph(filename: str) -> OsmnxGraph: ...
    # retorna el graf guardat al fitxer filename


def build_city_graph(g1: OsmnxGraph, g2: MetroGraph) -> CityGraph: ...
    # retorna un graf fusió de g1 i g2


Coord = (float, float)   # (latitude, longitude)


NodeID = Union[int, str]
Path = List[NodeID]

def find_path(ox_g: OsmnxGraph, g: CityGraph, src: Coord, dst: Coord) -> Path: ...


def show(g: CityGraph) -> None: ...
    # mostra g de forma interactiva en una finestra
def plot(g: CityGraph, filename: str) -> None: ...
    # desa g com una imatge amb el mapa de la cuitat de fons en l'arxiu filename
def plot_path(g: CityGraph, p: Path, filename: str, ...) -> None: ...
    # mostra el camí p en l'arxiu filename
