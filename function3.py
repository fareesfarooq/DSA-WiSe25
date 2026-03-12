# F3: Calculate Delivery Capacity (Max Flow)
# This function determines the maximum number of drones that can simultaneously
# fly from a source hub to a destination using the EdmondKarp algorithm.
def calculate_max_flow(network, source_id, sink_id):

    # validate that both source and sink nodes exist in the network
    if source_id not in network.nodes or sink_id not in network.nodes:
        print(
            f"error: source '{source_id}' or sink '{sink_id}' does not exist")
        return

    # check to ensure source and sink are not the same
    if source_id == sink_id:
        print("error: source and destination cannot be the same")
        return

    print(f"calculating max flow from {source_id} to {sink_id}...")

    # 1. Build Residual Graph
    # create a local capacity map so we do not modify the actual network data
    # format: capacity[u][v] = available_capacity
    capacity = {}

    # initialize all potential connections with 0 capacity
    for u in network.nodes:
        capacity[u] = {}
        for v in network.nodes:
            capacity[u][v] = 0

    # fill in actual capacities from the network edges
    # we loop through the network adjacency list
    for u, edges in network.adjacency.items():
        for edge in edges:
            # only consider edges that are not blocked
            if not edge.blocked:
                capacity[u][edge.to_node] = edge.capacity

    # 2. Edmonds-Karp Algorithm
    max_flow = 0

    while True:
        # find a path using bfs (breadth-first search)
        parent = {node: None for node in network.nodes}
        queue = [source_id]
        path_found = False

        while queue:
            u = queue.pop(0)

            if u == sink_id:
                path_found = True
                break

            # check all neighbors of u
            for v in network.nodes:
                # if v is not visited and there is available residual capacity
                if parent[v] is None and capacity[u][v] > 0:
                    parent[v] = u
                    queue.append(v)

        # if no path is found, we are done
        if not path_found:
            break

        # calculate the bottleneck (min capacity) on this path
        path_flow = float('inf')
        v = sink_id
        while v != source_id:
            u = parent[v]
            path_flow = min(path_flow, capacity[u][v])
            v = u

        # update residual capacities
        # subtract flow from forward path, add to reverse path (residual)
        v = sink_id
        while v != source_id:
            u = parent[v]
            capacity[u][v] -= path_flow
            capacity[v][u] += path_flow
            v = u

        # add the bottleneck flow to the total max flow
        max_flow += path_flow

    # report resultsd
    print(f"\n[RESULT] max flow capacity: {max_flow} drones/hour")
    print(
        f"this is the maximum number of drones that can go from {source_id} to {sink_id} at once")
