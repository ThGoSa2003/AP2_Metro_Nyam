import networkx
import osmnx as ox
import haversine
import pandas as pd
import staticmap
from metro import Position, get_metro_graph, MetroGraph, Access, Station
import os
from typing import Optional, Tuple, List, Union, Dict
from dataclasses import dataclass
from typing_extensions import TypeAlias


@dataclass
class St_node:
    id: int
    pos: Position

    def __hash__(self):
        return hash(self.id)

CityGraph : TypeAlias = networkx.Graph
OsmnxGraph : TypeAlias = networkx.MultiDiGraph

def get_osmnx_graph() -> OsmnxGraph:
    """
    :returns: a networkx graph of the city of Barcelona
    """

    return ox.graph_from_place("Barcelona, Spain", network_type = "walk")

def save_osmnx_graph(g: OsmnxGraph, filename: str) -> None:
    """
    :param g: a graph that you want to save in a file
    :param filename: the path and name of the file you want to store the graph in
    :effect: g must be stored in filename with extension gpickle
    """

    networkx.write_gpickle(g, path = filename)

def load_osmnx_graph(filename: str) -> OsmnxGraph:
    """
    :param filename: the path of a graph that you want to load (must be .gpickle)
    :returns: the graph in filename
    """

    if not os.path.exists(filename):
        save_osmnx_graph(get_osmnx_graph(),filename)
    return networkx.read_gpickle(filename)

def save_city_graph(g: CityGraph, filename: str) -> None:
    """
    might get rid of this one
    """
    networkx.write_gpickle(g, path = filename)

def load_city_graph(filename_osmnx: str, filename_city: str) -> CityGraph:
    """
    :param filename_osmnx: a path to a graph of the streets of the city
    :param filename_city: a path to a complete graph of the city
    :returns: a graph of the city
    """

    if not os.path.exists(filename_city):
        save_city_graph(build_city_graph(load_osmnx_graph(filename_osmnx),get_metro_graph()),filename_city)
    return networkx.read_gpickle(filename_city)


def build_city_graph(g1: OsmnxGraph, g2: MetroGraph) -> CityGraph:
    """
    :param g1: a graph of the streets of a city
    :param g2: a graph of the metro of a city
    :returns: a union of g1 and g2 that joins some of the accesses and street nodes
    """

    city_graph = networkx.Graph()
    metro_nodes = [node for node in g2.nodes]

    st_nodes_dict = {k : St_node(k, (v['x'], v['y'])) for k, v in g1.nodes.data()}
    st_nodes = [St_node(k, (v['x'], v['y'])) for k, v in g1.nodes.data()]
    st_nodes.sort(key = lambda s : (s.id)) # try without this
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


Coord : TypeAlias = Tuple[float, float]   # (latitude, longitude)


Node : TypeAlias = Union[Access, Station]
Path : TypeAlias = List[Node]


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
    """
    :param g: a graph of the city
    :param filename: a path to a file in the system
    :effect: It will store an image of g in filename. For different types of nodes and edges
    the colours will be different.
    """

    map = staticmap.StaticMap(3000, 3000)
    colour = {Access : "black", St_node: "brown", "L1": "red","L2": "darkviolet","L3": "green","L4": "gold","L5": "blue","L9N": "orangered","L9S": "orangered","L10N": "darkturquoise","L10S": "darkturquoise","L11": "greenyellow","FM": "forestgreen"}
    for node in g.nodes:
        if type(node) == Station:
            map.add_marker(staticmap.CircleMarker(node.pos, colour[node.line], 1))
        else:
            map.add_marker(staticmap.CircleMarker(node.pos, colour[type(node)], 1))
    for edge in g.edges.data():
        if edge[2]['type'] == 'tram':
            map.add_line(staticmap.Line([edge[0].pos, edge[1].pos], colour[edge[0].line], 0))
        else:
            map.add_line(staticmap.Line([edge[0].pos, edge[1].pos], "firebrick", 0))
    image = map.render()
    image.save(filename)

def plot_path(g: CityGraph, p: Path, filename: str) -> None:

    map = staticmap.StaticMap(3000, 3000)
    colour = {Access : "black", St_node: "brown", "L1": "red","L2": "darkviolet","L3": "green","L4": "gold","L5": "blue","L9N": "orangered","L9S": "orangered","L10N": "darkturquoise","L10S": "darkturquoise","L11": "greenyellow","FM": "forestgreen"}
    for i in range(len(p) - 1):
        if type(p[i]) == Station and type(p[i+1]) == Station:
            map.add_line(staticmap.Line((p[i].pos,p[i + 1].pos), colour[p[i].line], 3))
        else:
            map.add_line(staticmap.Line((p[i].pos,p[i + 1].pos), colour[p[i]], 3))
    for node in p:
        if type(node) == Station:
            map.add_marker(staticmap.CircleMarker(node.pos, colour[node.line], 10))
        else:
            map.add_marker(staticmap.CircleMarker(node.pos, colour[node], 10))
    image = map.render()
    image.save(filename)

c_t = load_city_graph("./graph.gpickle","./city_graph.gpickle")
o_g = load_osmnx_graph("./graph.gpickle")
plot(c_t,"./Cit.png" )
#plot_path(c_t, find_path(o_g,c_t,(2.0713,41.2877),(2.1986,41.4592)),"./Cit") # there is a bug here for some reason
# some nodes from osmnx have not been added, must fix build_city_graph
