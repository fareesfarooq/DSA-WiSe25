import json
from collections import defaultdict


class Node:
    def __init__(self, node_id, node_type):
        self.id = node_id
        self.type = node_type

    def __repr__(self):
        return f"Node({self.id}, {self.type})"


class Edge:
    def __init__(self, from_node, to_node, energy, capacity, bidirectional=False):
        self.from_node = from_node
        self.to_node = to_node
        self.energy = energy
        self.capacity = capacity
        self.bidirectional = bidirectional
        self.blocked = False  # used to disable a path if needed later

    def __repr__(self):
        direction = "<->" if self.bidirectional else "->"
        status = "(blocked)" if self.blocked else ""
        return f"{self.from_node} {direction} {self.to_node} [E={self.energy}, C={self.capacity}] {status}"


class DroneNetwork:
    """
    main class that stores the drone network.
    handles nodes, edges and how everything is connected.
    """

    def __init__(self):
        self.nodes = {}              # stores nodes by id
        self.edges = []              # list of all edges in the network
        self.adjacency = defaultdict(list)  # helps with traversal and lookups

    # B1: Input drone network from a JSON file
    # reads nodes and flight corridors including direction, energy and capacity
    def load_from_json(self, filename):
        print(f"trying to load network from file: {filename}")
        try:
            with open(filename, 'r') as file:
                data = json.load(file)

            # create all nodes first (charging stations, hubs, delivery points)
            for node_data in data['nodes']:
                self.nodes[node_data['id']] = Node(
                    node_data['id'],
                    node_data['type']
                )

            # then add flight corridors between nodes
            for edge_data in data['edges']:
                self.add_edge_internal(
                    edge_data['from'],
                    edge_data['to'],
                    edge_data['energy'],
                    edge_data['capacity'],
                    edge_data.get('bidirectional', False)
                )

            print(
                f"loaded {len(self.nodes)} nodes and {len(self.edges)} edges")

        except FileNotFoundError:
            print(f"file '{filename}' was not found, check the name")
        except json.JSONDecodeError:
            print(f"file '{filename}' is not valid json")

    # B3: extend and modify the drone network (adding corridors)
    # adds a new flight corridor and updates adjacency structure
    def add_edge_internal(self, from_id, to_id, energy, capacity, bidirectional):
        edge = Edge(from_id, to_id, energy, capacity, bidirectional)
        self.edges.append(edge)
        self.adjacency[from_id].append(edge)

        if bidirectional:
            # if corridor is usable both ways, add reverse edge
            reverse_edge = Edge(to_id, from_id, energy,
                                capacity, bidirectional)
            self.edges.append(reverse_edge)
            self.adjacency[to_id].append(reverse_edge)

    # B2: Define no-fly zones (basic)
    # blocks a specific corridor between two nodes
    def block_edge(self):
        u = input("enter start node id to block: ")
        v = input("enter end node id to block: ")

        found = False
        for edge in self.adjacency[u]:
            if edge.to_node == v:
                edge.blocked = True
                found = True
                print(f"path {u} -> {v} has been blocked")

        if not found:
            print("path not found, nothing was blocked")

    # B3: extend the drone network (adding nodes)
    # allows new nodes such as buildings or charging stations
    def add_node_menu(self):
        nid = input("enter node id: ")
        ntype = input("enter node type (distributor/delivery/charging): ")

        if nid in self.nodes:
            print("node already exists")
        else:
            self.nodes[nid] = Node(nid, ntype)
            print(f"node {nid} added")

    # utility function to show current network state
    def print_summary(self):
        print(
            f"\nnetwork summary: {len(self.nodes)} nodes, {len(self.edges)} edges")
        print("nodes currently in the network:")
        for n in self.nodes.values():
            print(f" - {n}")
