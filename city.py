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
    id: int
    pos: Position

    def __hash__(self):
        return hash(self.id)

St_nodes = List[St_node]

def build_city_graph(g1: OsmnxGraph, g2: MetroGraph) -> CityGraph:

    city_graph = networkx.Graph()

    metro_nodes = [node[0] for node in g2.nodes.data()]
    st_nodes_dict = {k : St_node(k, (v['x'], v['y'])) for k, v in g1.nodes.data()}

    st_nodes = [St_node(k, (v['x'], v['y'])) for k, v in g1.nodes.data()]
    st_nodes.sort(key = lambda s : (s.id))

    city_graph.add_nodes_from(metro_nodes)
    city_graph.add_nodes_from(st_nodes)
    city_graph.add_edges_from(g2.edges.data())

    for edge_n_atribiute in g1.edges.data():
        if 'name' in edge_n_atribiute[2]:
            city_graph.add_edge(edge_n_atribiute[0],edge_n_atribiute[1],distance = edge_n_atribiute[2]['length'], street_name = edge_n_atribiute[2]['name'])
        else:
            city_graph.add_edge(edge_n_atribiute[0],edge_n_atribiute[1],distance = edge_n_atribiute[2]['length'])

<<<<<<< HEAD
=======
    for node in g2.nodes.data():
        print(type(node[0]) is Access, " A: ", node[0])
        if type(node[0]) is Access:
            closest_st_node = ox.distance.nearest_nodes(g1, node[0].pos[0], node[0].pos[1])
            city_graph.add_edge(node[0], st_nodes_dict[closest_st_node], type = "walk", distance = distance(node[0], st_nodes_dict[closest_st_node]))
    return city_graph
show(build_city_graph(load_osmnx_graph("./graph"),get_metro_graph()))
>>>>>>> ce7ad2d142f84a39cca6c0e234ce775f575e3c97
    for node in g2.nodes:
        if type(node) is Access:
            closest_st_node = ox.distance.nearest_nodes(g1, node.pos[0], node.pos[1])
            print(closest_st_node)
            city_graph.add_edge(node, st_nodes_dict[closest_st_node], type = "walk", distance = distance(node, st_nodes_dict[closest_st_node]))

build_city_graph(load_osmnx_graph("./graph"),get_metro_graph())
>>>>>>> 444d24c3b43df4929797380c8e88ff5bc3b2f353

Coord = (float, float)   # (latitude, longitude)


Node = Union[Access, Station, Dict[int:Dict[str:int]]]
Path = List[Node]
"""
def find_closest_node(g: Optional[City_graph], src: Coord) -> :
    min = float("inf")
    closest_node = 0
    for node in g.nodes():
        distance = ((src[0] - node.pos[0])**2 + (src[1] - node.pos[1])**2)**1/2
        if distance < min:
            min = distance
            closest_node = node
    return closest_node
"""

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
    node_map = {node.id: node for node in g.nodes.data()}
    edge_map = {(edge[0], edge[1])}
    for nodeid in p:
        map.add_marker(staticmap.CircleMarker(node_map[nodeid].pos, "red", 10))
    for i in range():...
