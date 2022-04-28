import networkx
import staticmap
import pandas as pd


def get_metro_graph() -> MetroGraph: ...


MetroGraph = networkx.Graph


@dataclass
class Station: ...

@dataclass
class Access: ...

Stations = List[Station]

Accesses = List[Access]


def read_stations() -> Stations:

    csv_estacions = pd.read_csv('https://raw.githubusercontent.com/jordi-petit/ap2-metro-nyam-2022/main/data/blob/main/estacions.csv')

def read_accesses() -> Accesses:

    csv_accessos = pd.read_csv('https://raw.githubusercontent.com/jordi-petit/ap2-metro-nyam-2022/main/data/blob/main/accessos.csv')


def show(g: MetroGraph) -> None: ...
def plot(g: MetroGraph, filename: str) -> None: ...
