from matplotlib import pyplot as plt
import networkx
import osmnx as ox
import haversine
import pandas as pd
import staticmap
import constants as ct
from metro import Position, get_metro_graph, MetroGraph
import os
from typing import Dict
from nodes import *

CityGraph: TypeAlias = networkx.Graph
OsmnxGraph: TypeAlias = networkx.MultiDiGraph


def get_osmnx_graph() -> OsmnxGraph:
    """
    :returns: a networkx graph of the city of Barcelona
    """

    return ox.graph_from_place("Barcelona, Spain", network_type="walk")


def save_osmnx_graph(g: OsmnxGraph, filename: str) -> None:
    """
    :param g: a graph that you want to save in a file
    :param filename: the name of the file you want to store the graph in
    :effect: g must be stored in filename with extension gpickle
    """

    networkx.write_gpickle(g, path=filename)


def load_osmnx_graph(filename: str) -> OsmnxGraph:
    """
    :param filename: the path of the graph to be loaded (must be .gpickle)
    :returns: the graph in filename
    """

    if not os.path.exists(filename):
        save_osmnx_graph(get_osmnx_graph(), filename)
    return networkx.read_gpickle(filename)


def save_city_graph(g: CityGraph, filename: str) -> None:
    """
    :param g: a graph of the city
    :param filename: a file where to store the graph
    :effect: an image of g is stored in filename
    """

    networkx.write_gpickle(g, path=filename)


def load_city_graph(filename_osmnx: str, filename_city: str) -> CityGraph:
    """
    :param filename_osmnx: a path to a graph of the streets of the city
    :param filename_city: a path to a complete graph of the city
    :returns: a graph of the city
    """

    if not os.path.exists(filename_city):
        save_city_graph(build_city_graph(load_osmnx_graph(filename_osmnx),
                                         get_metro_graph()),
                        filename_city)
    return networkx.read_gpickle(filename_city)


def build_city_graph(g1: OsmnxGraph, g2: MetroGraph) -> CityGraph:
    """
    :param g1: a graph of the streets of a city
    :param g2: a graph of the metro of a city
    :returns: a union of g1 and g2 that joins some of the accesses and street nodes
    :warning: nodes are stored as hashable classes
    """

    city_graph = networkx.Graph()
    metro_nodes = [node for node in g2.nodes]

    st_nodes_dict = {k: St_node(k, (v['x'], v['y']))
                     for k, v in g1.nodes.data()}
    st_nodes = [St_node(k, (v['x'], v['y'])) for k, v in g1.nodes.data()]
    city_graph.add_nodes_from(st_nodes)

    for edge_n_attribute in g1.edges.data():
        if(edge_n_attribute[0] != edge_n_attribute[1]):
            node1 = st_nodes_dict[edge_n_attribute[0]]
            node2 = st_nodes_dict[edge_n_attribute[1]]
            if 'name' in edge_n_attribute[2]:
                city_graph.add_edge(node1, node2,
                                    distance=edge_n_attribute[2]['length'],
                                    street_name=edge_n_attribute[2]['name'],
                                    type="walk")
            else:
                city_graph.add_edge(node1, node2,
                                    distance=edge_n_attribute[2]['length'],
                                    type="walk")

    city_graph.add_edges_from(g2.edges.data())
    city_graph.add_nodes_from(metro_nodes)

    for node in g2.nodes.data():
        if type(node[0]) is Access:
            closest_st_node = ox.distance.nearest_nodes(g1, node[0].pos[0],
                                                        node[0].pos[1])
            city_graph.add_edge(node[0], st_nodes_dict[closest_st_node],
                                type="walk", distance=distance(node[0],
                                st_nodes_dict[closest_st_node]))

    return city_graph


def find_path(ox_g: OsmnxGraph, g: CityGraph, src: Position, dst: Position) -> Path:
    """
    :param ox_g: a graph of the streets of the city.
    :param g: a graph of the city
    :param src: the starting node.
    :param dst: the enging node.
    :returns: the shortest path from src to dst.
    """

    src_node = ox.distance.nearest_nodes(ox_g, src[0], src[1])
    dst_node = ox.distance.nearest_nodes(ox_g, dst[0], dst[1])
    for node in g.nodes:
        if type(src_node) == int or type(dst_node) == int:
            if src_node == node.id:
                src_node = node
            if dst_node == node.id:
                dst_node = node
        else:
            break

    def w(n1, n2, d): return d['distance']/ct.velocity[d['type']]
    return networkx.shortest_path(g, src_node, dst_node, weight=w)


def show(g: CityGraph) -> None:
    """
    :param g: a graph of the city.
    :effect: a plot of the hole city will be optuped as an image.
    """

    positions = {}
    for n in networkx.nodes(g):
        positions[n] = n.pos
    networkx.draw_networkx(g, pos=positions, node_size=10, with_labels=False)
    plt.show()


def plot(g: CityGraph, filename: str) -> None:
    """
    :param g: a graph of the city
    :param filename: a path to a file in the system
    :effect: It will store an image of g in filename.
             For different types of nodes and edges
    the colours will be different.
    """

    map = staticmap.StaticMap(ct.resolution_x, ct.resolution_y)
    for node in g.nodes:
        if type(node) == Station:
            map.add_marker(staticmap.CircleMarker(node.pos,
                                                  ct.colour[node.line],
                                                  1))
        else:
            map.add_marker(staticmap.CircleMarker(node.pos,
                                                  ct.colour["other"],
                                                  1))
    for edge in g.edges.data():
        if edge[2]['type'] == 'tram':
            map.add_line(staticmap.Line([edge[0].pos, edge[1].pos],
                                        ct.colour[edge[0].line], 0))
        else:
            map.add_line(staticmap.Line([edge[0].pos, edge[1].pos],
                                        ct.colour["other"], 0))
    image = map.render()
    image.save(filename)


def plot_path(g: CityGraph, p: Path, filename: str) -> None:
    """
    :param g: a graph of the city.
    :param p: a path inside of the graph
    :effect: saves an image of the path in filename
    """

    map = staticmap.StaticMap(ct.resolution_x, ct.resolution_y)
    for i in range(len(p) - 1):
        if type(p[i]) == Station and type(p[i+1]) == Station and p[i].line == p[i+1].line:
            map.add_line(staticmap.Line((p[i].pos, p[i + 1].pos),
                                        ct.colour[p[i].line], 3))
        else:
            map.add_line(staticmap.Line((p[i].pos, p[i + 1].pos),
                                        ct.colour["other"], 3))
    for node in p:
        if type(node) == Station:
            map.add_marker(staticmap.CircleMarker(node.pos,
                                                  ct.colour[node.line], 10))
        else:
            map.add_marker(staticmap.CircleMarker(node.pos,
                                                  ct.colour["other"], 10))
    image = map.render()
    image.save(filename)
