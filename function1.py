# F1: Check Reachability
# This function verifies whether all assigned delivery points in a given drone network are rseachable from a distribution hub using BFS
def check_reachability(network, start_node_id):

    # validate that the start node actually exists in the network
    if start_node_id not in network.nodes:
        print(f"error: node '{start_node_id}' does not exist")
        return

    print(f"checking reachability starting from {start_node_id}...")

    # 1. Initialize BFS
    # visited set tracks where we have been to avoid loops
    visited = set()
    queue = [start_node_id]
    visited.add(start_node_id)

    # 2. Traverse the graph
    # loops as long as there are nodes in the queue to explore
    while queue:
        current_node = queue.pop(0)

        # look up the edges for the current node using the network's adjacency list
        if current_node in network.adjacency:
            for edge in network.adjacency[current_node]:
                # check if the path is NOT blocked and we haven't visited the neighbor yet
                if not edge.blocked and edge.to_node not in visited:
                    visited.add(edge.to_node)
                    queue.append(edge.to_node)

    # 3. Verify delivery points
    # identify all nodes that are specifically marked as 'delivery'
    all_delivery_nodes = [
        nid for nid, node in network.nodes.items()
        if node.type == "delivery"
    ]

    # filter for delivery nodes that were NOT found in our visited set
    unreachable = [nid for nid in all_delivery_nodes if nid not in visited]

    # 4. Report results
    if not unreachable:
        print(
            f"\n[SUCCESS] all delivery points are reachable from {start_node_id}")
    else:
        print(
            f"\n[WARNING] the following delivery points are UNREACHABLE from {start_node_id}:")
        for nid in unreachable:
            print(f" - {nid}")
