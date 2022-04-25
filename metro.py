import networkx
import staticmap

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
