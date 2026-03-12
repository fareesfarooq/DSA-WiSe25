import heapq

# F2: Efficient Flight Routes (Shortest Path)
# This function finds the minimum energy path between two nodes
# using Dijkstra's algorithm, while ignoring blocked corridors.

def find_efficient_route(network, start_id, goal_id, required_capacity=1):
    # Validation Check
    if start_id not in network.nodes or goal_id not in network.nodes:
        print(f"error: start '{start_id}' or goal '{goal_id}' does not exist")
        return

    if start_id == goal_id:
        print("start and goal are the same; route energy = 0")
        print(f"Route: {start_id}")
        return

    # dist[node] = best known energy cost to reach node
    dist = {node_id: float("inf") for node_id in network.nodes}
    dist[start_id] = 0

    # parent[node] = previous node on best path
    parent = {node_id: None for node_id in network.nodes}

    # min-heap of (current_energy, node_id)
    pq = [(0, start_id)]

    while pq:
        current_energy, u = heapq.heappop(pq)

        # If this is an outdated heap entry, skip it
        if current_energy > dist[u]:
            continue

        # Early exit once we reach the goal
        if u == goal_id:
            break

        # Explore outgoing edges from u
        for edge in network.adjacency.get(u, []):
            # Skip blocked edges (no-fly zones)
            if edge.blocked:
                continue

            # enforce capacity constraint
            if edge.capacity < required_capacity:
                continue

            v = edge.to_node
            new_energy = current_energy + edge.energy

            if new_energy < dist[v]:
                dist[v] = new_energy
                parent[v] = u
                heapq.heappush(pq, (new_energy, v))

    # Reconstruct path
    if dist[goal_id] == float("inf"):
        print(f"\n[WARNING] No available route from {start_id} to {goal_id}.")
        print("Reason: graph disconnected, or all routes blocked / insufficient capacity.")
        return

    path = []
    cur = goal_id
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()

    # Compute botttleneck capacity along the chosen path (min capacity on path)
    bottleneck = float("inf")
    for i in range(len(path) - 1):
        a, b = path[i], path[i + 1]
        # find the actual edge used (a-->b) to read its capacity
        for e in network.adjacency[a]:
            if e.to_node == b and not e.blocked:
                bottleneck = min(bottleneck, e.capacity)
                break

    print(f"\n[RESULT] Most energy-efficient route from {start_id} to {goal_id}:")
    print(" -> ".join(path))
    print(f"Total energy cost: {dist[goal_id]}")
    if bottleneck != float("inf"):
        print(f"Bottleneck capacity on this route: {bottleneck}")
