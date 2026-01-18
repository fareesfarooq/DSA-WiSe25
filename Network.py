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

            print(f"loaded {len(self.nodes)} nodes and {len(self.edges)} edges")

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
            reverse_edge = Edge(to_id, from_id, energy, capacity, bidirectional)
            self.edges.append(reverse_edge)
            self.adjacency[to_id].append(reverse_edge)

    # NEW: Add corridor via menu (so new nodes can be connected)
    def add_corridor_menu(self):
        from_id = input("from node id: ")
        to_id = input("to node id: ")

        if from_id not in self.nodes or to_id not in self.nodes:
            print("one or both nodes do not exist. add them first.")
            return

        try:
            energy = float(input("energy cost: "))
            capacity = int(input("capacity: "))
        except ValueError:
            print("invalid energy/capacity input.")
            return

        bidir = input("bidirectional? (y/n): ").strip().lower() == "y"
        self.add_edge_internal(from_id, to_id, energy, capacity, bidir)
        print(f"corridor added: {from_id} {'<->' if bidir else '->'} {to_id}")

    # B2: Define no-fly zones (basic)
    # blocks a specific corridor between two nodes
    def block_edge(self):
        u = input("enter start node id to block: ")
        v = input("enter end node id to block: ")

        if u not in self.nodes or v not in self.nodes:
            print("one or both nodes do not exist.")
            return

        found = False
        for edge in self.adjacency.get(u, []):
            if edge.to_node == v:
                edge.blocked = True
                found = True
                print(f"path {u} -> {v} has been blocked")

        if not found:
            print("path not found, nothing was blocked")

    # B3: extend the drone network (adding nodes)
    # allows new nodes such as buildings or charging stations
    # UPDATED: offers connecting the node right away
    def add_node_menu(self):
        nid = input("enter node id: ")
        ntype = input("enter node type (distributor/delivery/charging): ")

        if nid in self.nodes:
            print("node already exists")
            return

        self.nodes[nid] = Node(nid, ntype)
        print(f"node {nid} added")

        connect = input("do you want to connect this node now? (y/n): ").strip().lower()
        while connect == "y":
            from_id = input("connect FROM node id: ")
            if from_id not in self.nodes:
                print("that node does not exist.")
                continue

            try:
                energy = float(input("energy cost: "))
                capacity = int(input("capacity: "))
            except ValueError:
                print("invalid energy/capacity input.")
                continue

            bidir = input("bidirectional? (y/n): ").strip().lower() == "y"
            self.add_edge_internal(from_id, nid, energy, capacity, bidir)

            print(f"connected {from_id} {'<->' if bidir else '->'} {nid}")
            connect = input("add another connection to this node? (y/n): ").strip().lower()

    # utility function to show current network state
    def print_summary(self):
        print(f"\nnetwork summary: {len(self.nodes)} nodes, {len(self.edges)} edges")
        print("nodes currently in the network:")
        for n in self.nodes.values():
            print(f" - {n}")
