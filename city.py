import networkx
import osmnx as ox
import haversine
import pandas
import pandas as pd
import staticmap
from metro import *
import os
from typing import Optional, Tuple, List, Union

CityGraph = networkx.Graph
OsmnxGraph = networkx.MultiDiGraph


def get_osmnx_graph() -> OsmnxGraph:
    return ox.graph_from_place("Barcelona, Spain", network_type = "walk")

def save_osmnx_graph(g: OsmnxGraph, filename: str) -> None:
    networkx.write_gpickle(g, path=filename+".gpickle")

def load_osmnx_graph(filename: str) -> OsmnxGraph:
    if not os.path.exists(filename + ".gpickle"):
        save_osmnx_graph(get_osmnx_graph(),filename)
    osmnx_graph =  networkx.read_gpickle(filename + ".gpickle")
    return osmnx_graph

@dataclass
class St_node:
    id_node: int
    pos: Position

    def __hash__(self):
        return hash(self.id_node)

St_nodes = List[St_node]

def build_city_graph(g1: OsmnxGraph, g2: MetroGraph) -> CityGraph:

    city_graph = nx.Graph()
    metro_nodes = [node for node in g2.nodes.data()]
    st_nodes = [St_node(k, (v.x, v.y)) for k, v in g1.nodes.data()]
    st_nodes.sort(key = lambda s : (s.id_node))
    city_graph.add_nodes_from(metro_nodes)
    city_graph.add_nodes_from(st_nodes)
    for edge in g1.edge.data():
        city_graph.add_edge(edge)
    for edge in g2.edge.data():
        city_graph.add_edge(st_nodes[edge[0]], st_nodes[edge[1]], type="walk", distance=edge[2].length)
        city_graph.add_edge(st_nodes[edge[1]], st_nodes[edge[2]], type="walk", distance=edge[2].length)
    for node in g2.nodes:
        if type(node) is Access:
            closest_st_node = ox.distance.nearest_nodes(g1, node.pos[0], node.pos[1])
            city_graph.add_edge(node, st_nodes[closest_st_node], type = "walk", distance = distance(node, st_nodes[closest_st_node]))
            city_graph.add_edge(node, st_nodes[closest_st_node], type = "walk", distance = distance(node, st_nodes[closest_st_node]))

Coord = (float, float)   # (latitude, longitude)


Node = Union[Access, Station, Dict[int:Dict[str:int]]]
Path = List[Node]

def find_closest_node(g: Optional[City_graph], src: Coord) -> :
    min = float("inf")
    closest_node = 0
    for node in g.nodes():
        distance = ((src[0] - node.pos[0])**2 + (src[1] - node.pos[1])**2)**1/2
        if distance < min:
            min = distance
            closest_node = node
    return closest_node


def find_path(ox_g: OsmnxGraph, g: CityGraph, src: Coord, dst: Coord) -> Path:
    src_node = osmnx.distance.nearest_nodes(ox_g,src[0],src[1])
    dst_node = osmnx.distance.nearest_nodes(ox_g,dst[0],dst[1])

def show(g: CityGraph) -> None:
    positions = {}
    for n in nx.nodes(g):
        positions[n] = n.pos
    nx.draw_networkx(g,pos = positions, node_size = 10, with_labels = False)
    plt.show()

def plot(g: CityGraph, filename: str) -> None:
    map = staticmap.StaticMap(1980, 1080)
    for node in g.nodes:
        map.add_marker(staticmap.CircleMarker(node.pos, "red", 10))
    for edge in g.edges:
        map.add_line(staticmap.Line([edge[0].pos, edge[1].pos], "blue", 5))
    image = map.render()
    image.save(filename + ".png")

def plot_path(g: CityGraph, p: Path, filename: str) -> None:
    map = staticmap.StaticMap(1980, 1080)
    for nodeid in p:
