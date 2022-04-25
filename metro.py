import networkx
import staticmap
import pandas as pd

url = 'https://raw.githubusercontent.com/jordi-petit/ap2-metro-nyam-2022/main/data/restaurants.csv'
csv_restaurants = pd.read_csv(url)
url = 'https://raw.githubusercontent.com/jordi-petit/ap2-metro-nyam-2022/main/data/blob/main/estacions.csv'
csv_restaurants = pd.read_csv(url)
url = 'https://raw.githubusercontent.com/jordi-petit/ap2-metro-nyam-2022/main/data/blob/main/accessos.csv'
csv_restaurants = pd.read_csv(url)


def get_metro_graph() -> MetroGraph: ...


MetroGraph = networkx.Graph


@dataclass
class Station: ...

@dataclass
class Access: ...

Stations = List[Station]

Accesses = List[Access]


def read_stations() -> Stations: ...
def read_accesses() -> Accesses: ...


def show(g: MetroGraph) -> None: ...
def plot(g: MetroGraph, filename: str) -> None: ...
