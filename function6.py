import heapq

def find_communication_network(network):
        """
        This function finds the cheapest way to connect all drone stations with communication links.
        We use a method called Minimum Spanning Tree (MST) to do this.
        
        Arguments:
        network (DroneNetwork): The network containing all drone stations and possible communication links.
        
        Returns:
        list of edges: The edges that form the cheapest communication network.
        """
        # Start with an empty list to hold the edges we select for the communication network
        mst_edges = []
        
        # Create a priority queue (min-heap) to always pick the cheapest edge
        min_heap = []
        
        # Let's start from the first node in the network
        first_node = next(iter(network.nodes.values()))
        
        # Keep track of which nodes we've added to the network
        visited = set()
        visited.add(first_node.id)
        
        # Add all edges connected to the starting node to the min-heap
        def add_edges(node_id):
            for edge in network.adjacency[node_id]:
                if edge.to_node not in visited:
                    # Add edge to the heap with its cost (energy)
                    heapq.heappush(min_heap, (edge.energy, edge))
        
        # Add edges of the starting node to the min-heap
        add_edges(first_node.id)
        
        while min_heap:
            # Pop the edge with the lowest cost (energy)
            energy, edge = heapq.heappop(min_heap)
            
            # If the destination node is already in the network, skip this edge
            if edge.to_node in visited:
                continue
            
            # Add this edge to the MST and mark the destination node as visited
            mst_edges.append(edge)
            visited.add(edge.to_node)
            
            # Add all edges connected to the new node to the heap
            add_edges(edge.to_node)
        
        # Calculate the total cost (energy) of the MST
        total_cost = sum(edge.energy for edge in mst_edges)
        
        # Print the result
        print("\nCommunication network (MST) with the lowest cost:")
        for edge in mst_edges:
            print(edge)
        print(f"Total cost: {total_cost}")
        
        return mst_edges