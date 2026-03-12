# F4: Assess and Improve Network Resilience 
# if there is an edge u -> v (or v -> u), we assume u and v are connected for the purpose of bridge finding.
# We then use Tarjan's bridge-finding algorithm on this undirected view.

def find_critical_edges(network):
    # Build an undirected adjacency view from the directed graph
    undirected_adj = {node: [] for node in network.nodes}

    for u in network.nodes:
     for edge in network.adjacency.get(u, []):
        if edge.blocked:
            continue
        v = edge.to_node
        undirected_adj[u].append(v)
        undirected_adj[v].append(u)


    # Helper function: Depth-First Search (DFS) for bridges (Tarjan)
    def dfs(u, visited, discovery, low, parent, time_counter, bridges):
        visited[u] = True
        discovery[u] = low[u] = time_counter[0]
        time_counter[0] += 1

        # Visit all adjacent nodes (UNDIRECTED)
        for v in undirected_adj[u]:
            if not visited[v]:
                parent[v] = u
                dfs(v, visited, discovery, low, parent, time_counter, bridges)

                # Update low-link value
                low[u] = min(low[u], low[v])

                # Bridge condition in undirected graphs
                if low[v] > discovery[u]:
                    # Store consistently to avoid duplicates like (u,v) and (v,u)
                    bridges.append(tuple(sorted((u, v))))

            elif v != parent[u]:
                low[u] = min(low[u], discovery[v])

    # Initialize data structures
    visited = {node: False for node in network.nodes}
    discovery = {node: float('inf') for node in network.nodes}
    low = {node: float('inf') for node in network.nodes}
    parent = {node: None for node in network.nodes}
    time_counter = [0]
    bridges = []

    # Run DFS for each unvisited node
    for node in network.nodes:
        if not visited[node]:
            dfs(node, visited, discovery, low, parent, time_counter, bridges)

    # Remove duplicates (safety) and report
    bridges = sorted(set(bridges))

    if bridges:
        print("\n[RESULT] Critical Edges (Bridges) in the Network (Undirected Resilience View):")
        for (a, b) in bridges:
            print(f"  - {a} <-> {b}")
    else:
        print("\n[INFO] No critical edges found (the network is resilient under undirected connectivity).")
