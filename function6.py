import heapq


def find_communication_network(network):
    """
    F6: Communication Infrastructure (MST / Prim)

    Builds a minimum-cost set of links that connects all stations (if possible).
    Uses Prim's algorithm with a min-heap (priority queue).
    """

    # Edge case: empty network
    if not network.nodes:
        print("No nodes in network. Nothing to connect.")
        return []

    mst_edges = []
    min_heap = []

    # Start from an arbitrary node
    first_node = next(iter(network.nodes.values()))
    visited = set([first_node.id])

    # Tie-breaker counter to avoid Python comparing Edge objects
    push_id = 0

    def add_edges(node_id):
        nonlocal push_id
        for edge in network.adjacency.get(node_id, []):
            # Optional safety: ignore blocked links if you treat them as unavailable
            if getattr(edge, "blocked", False):
                continue

            if edge.to_node not in visited:
                push_id += 1
                # (cost, tie_breaker, edge)
                heapq.heappush(min_heap, (edge.energy, push_id, edge))

    add_edges(first_node.id)

    while min_heap and len(visited) < len(network.nodes):
        energy, _, edge = heapq.heappop(min_heap)

        if edge.to_node in visited:
            continue

        mst_edges.append(edge)
        visited.add(edge.to_node)
        add_edges(edge.to_node)

    # Disconnected network check
    if len(visited) != len(network.nodes):
        print("\n[WARNING] Communication network cannot connect all stations.")
        print(f"Connected {len(visited)} out of {len(network.nodes)} nodes.")
        print("Result is a minimum spanning forest for the reachable component(s).")

    total_cost = sum(edge.energy for edge in mst_edges)

    print("\nCommunication network (MST) with the lowest cost:")
    for edge in mst_edges:
        print(edge)
    print(f"Total cost: {total_cost}")

    return mst_edges
