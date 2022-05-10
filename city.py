import networkx
import osmnx as ox
import haversine
import pandas as pd
import staticmap
from metro import *
import os
from typing import Optional, Tuple, List, Union, Dict

CityGraph = networkx.Graph
OsmnxGraph = networkx.MultiDiGraph


def get_osmnx_graph() -> OsmnxGraph:
    return ox.graph_from_place("Barcelona, Spain", network_type = "walk")

def save_osmnx_graph(g: OsmnxGraph, filename: str) -> None:
    networkx.write_gpickle(g, path=filename+".gpickle")

def load_osmnx_graph(filename: str) -> OsmnxGraph:
    if not os.path.exists(filename + ".gpickle"):
        save_osmnx_graph(get_osmnx_graph(),filename)
    return networkx.read_gpickle(filename + ".gpickle")

def save_city_graph(g: CityGraph, filename: str) -> None:
    networkx.write_gpickle(g, path=filename+".gpickle")

def load_city_graph(filename_osmnx: str, filename_city: str) -> CityGraph:
    if not os.path.exists(filename_city + ".gpickle"):
        save_city_graph(build_city_graph(load_osmnx_graph(filename_osmnx),get_metro_graph()),filename_city)
    return networkx.read_gpickle(filename_city + ".gpickle")

@dataclass
class St_node:
    id: int
    pos: Position

    def __hash__(self):
        return hash(self.id)

St_nodes = List[St_node]

def build_city_graph(g1: OsmnxGraph, g2: MetroGraph) -> CityGraph:

    city_graph = networkx.Graph()
    metro_nodes = [node for node in g2.nodes]

    st_nodes_dict = {k : St_node(k, (v['x'], v['y'])) for k, v in g1.nodes.data()}
    st_nodes = [St_node(k, (v['x'], v['y'])) for k, v in g1.nodes.data()]
    st_nodes.sort(key = lambda s : (s.id))
    city_graph.add_nodes_from(st_nodes)

    for edge_n_atribiute in g1.edges.data():
        if(edge_n_atribiute[0] != edge_n_atribiute[1]):
            node1 = st_nodes_dict[edge_n_atribiute[0]]
            node2 = st_nodes_dict[edge_n_atribiute[1]]
            if 'name' in edge_n_atribiute[2]:
                city_graph.add_edge(node1,node2,distance = edge_n_atribiute[2]['length'], street_name = edge_n_atribiute[2]['name'], type = "walk")
            else:
                city_graph.add_edge(node1,node2,distance = edge_n_atribiute[2]['length'], type = "walk")

    city_graph.add_edges_from(g2.edges.data())
    city_graph.add_nodes_from(metro_nodes)

    for node in g2.nodes.data():
        if type(node[0]) is Access:
            closest_st_node = ox.distance.nearest_nodes(g1, node[0].pos[0], node[0].pos[1])
            city_graph.add_edge(node[0], st_nodes_dict[closest_st_node], type = "walk", distance = distance(node[0], st_nodes_dict[closest_st_node]))

    return city_graph


Coord = (float, float)   # (latitude, longitude)


Node = Union[Access, Station]
Path = List[Node]


def find_path(ox_g: OsmnxGraph, g: CityGraph, src: Coord, dst: Coord) -> Path:

    def w(n1, n2, d):
        type = d['type']
        vel = 0
        if type == 'walk':
            vel = 2
        elif type == 'tram':
            vel = 10
        elif type == 'enllaç':
            vel = 10000
        elif type == 'acces':
            vel = 2
        else:
            vel = 1
        return d['distance'] / vel

    src_node = ox.distance.nearest_nodes(ox_g,src[0],src[1])
    dst_node = ox.distance.nearest_nodes(ox_g,dst[0],dst[1])
    print(src_node, dst_node)
    for node in g.nodes:
        if type(src_node) == int or type(dst_node) == int:
            if src_node == node.id:
                src_node = node
            if dst_node == node.id:
                dst_node = node
        else:
            break

    return networkx.shortest_path(g, src_node, dst_node, weight = w)

def show(g: CityGraph) -> None:
    positions = {}
    for n in nx.nodes(g):
        positions[n] = n.pos
    nx.draw_networkx(g,pos = positions, node_size = 10, with_labels = False)
    plt.show()

def plot(g: CityGraph, filename: str) -> None:
    map = staticmap.StaticMap(1980, 1080)
    for node in g.nodes:
        if type(node) == Station:
            map.add_marker(staticmap.CircleMarker(node.pos, "red", 1))
        if type(node) == Access:
            map.add_marker(staticmap.CircleMarker(node.pos, "black", 1))
        if type(node) == St_node:
            map.add_marker(staticmap.CircleMarker(node.pos, "green", 1))
    for edge in g.edges.data():
        if edge[2]['type'] == 'walk':
            map.add_line(staticmap.Line([edge[0].pos, edge[1].pos], "yellow", 0))
        elif edge[2]['type'] == 'tram':
            map.add_line(staticmap.Line([edge[0].pos, edge[1].pos], "blue", 0))
        else:
            map.add_line(staticmap.Line([edge[0].pos, edge[1].pos], "orange", 0))
    image = map.render()
    image.save(filename + ".png")

def plot_path(g: CityGraph, p: Path, filename: str) -> None:
    map = staticmap.StaticMap(8000, 8000)
    for i in range(len(p) - 1):
        if type(p[i]) == Station and type(p[i+1]) == Station:
            map.add_line(staticmap.Line((p[i].pos,p[i + 1].pos), 'red', 3))
        else:
            map.add_line(staticmap.Line((p[i].pos,p[i + 1].pos), 'black', 3))
    for node in p:
        if type(node) == Station:
            map.add_marker(staticmap.CircleMarker(node.pos, "red", 10))
        else:
            map.add_marker(staticmap.CircleMarker(node.pos, "black", 10))

    image = map.render()
    image.save(filename + ".png")

c_t = load_city_graph("./graph","./city_graph")
o_g = load_osmnx_graph("./graph")
plot(c_t,"./city_image")
#plot_path(c_t, find_path(o_g,c_t,(2.0713,41.2877),(2.1986,41.4592)),"./city_image") # there is a bug here for some reason
# some nodes from osmnx have not been added, must fix build_city_graph
