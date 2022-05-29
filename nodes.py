from dataclasses import dataclass
from typing_extensions import TypeAlias
from typing import Union, List, Tuple
import sys

Position: TypeAlias = Tuple[float, float]


@dataclass
class St_node:
    """
    This represents a street node.
    """

    id: int
    pos: Position

    def __hash__(self):
        return hash(self.id)


@dataclass
class Station:
    """
    This class represents a station within the metro of a city
    """

    id: int
    name: str
    order: int
    line: str
    pos: Position

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass
class Access:
    """
    This class represents an access point to the metro of a city
    """

    id: int
    name: str
    accessibility: bool
    name_station: str
    pos: Position

    def __hash__(self) -> int:
        return hash(self.id)


Stations: TypeAlias = List[Station]
Accesses: TypeAlias = List[Access]

Node: TypeAlias = Union[Access, Station, St_node]
Path: TypeAlias = List[Node]


def distance(pos1: Position, pos2: Position) -> float:
    """
    :param node1, node2: any class with attribute pos (latitude and longitude)
    :returns: the euclidean distance between node1 node2
    """

    try:
        d = (pos1[0] - pos2[0])**2 + \
            (pos1[1] - pos2[1])**2
        return d**(1/2)
    except AttributeError:
        txt = "You tried to get the distance between something "
        txt += "that isn't a position."
        raise AttributeError(txt)
        sys.exit()
