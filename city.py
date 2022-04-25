import networkx
import osmnx
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


def get_osmnx_graph() -> OsmnxGraph: ...


OsmnxGraph = networkx.MultiDiGraph


def save_osmnx_graph(g: OsmnxGraph, filename: str) -> None: ...
    # guarda el graf g al fitxer filename
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
