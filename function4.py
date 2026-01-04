# F4: Assess and Improve Network Resilience
# This function identifies critical edges (bridges) whose removal will split the network into disconnected parts.
def find_critical_edges(network):
    # Helper function: Depth-First Search (DFS)
    def dfs(u, visited, discovery, low, parent, time_counter, bridges):
        visited[u] = True
        discovery[u] = low[u] = time_counter[0]
        time_counter[0] += 1  # Increment time using list to maintain reference
        
        # Visit all adjacent nodes
        for edge in network.adjacency[u]:
            v = edge.to_node
            
            if not visited[v]:  # If v is not visited
                parent[v] = u
                dfs(v, visited, discovery, low, parent, time_counter, bridges)
                
                # Check if the subtree rooted at v has a connection back to one of u's ancestors
                low[u] = min(low[u], low[v])
                
                # If the lowest vertex reachable from v is below u in DFS tree, then u-v is a critical edge
                if low[v] > discovery[u]:
                    bridges.append((u, v))
            
            elif v != parent[u]:  # If v is already visited and is not parent
                low[u] = min(low[u], discovery[v])
    
    # Initialize data structures
    visited = {node: False for node in network.nodes}
    discovery = {node: float('inf') for node in network.nodes}
    low = {node: float('inf') for node in network.nodes}
    parent = {node: None for node in network.nodes}
    time_counter = [0]  # Use list to maintain reference across recursive calls
    bridges = []
    
    # Run DFS for each unvisited node to find critical edges
    for node in network.nodes:
        if not visited[node]:
            dfs(node, visited, discovery, low, parent, time_counter, bridges)
    
    # Report the result
    if bridges:
        print("\n[RESULT] Critical Edges (Bridges) in the Network:")
        for edge in bridges:
            print(f"  - {edge[0]} -> {edge[1]}")
    else:
        print("\n[INFO] No critical edges found (the network is resilient).")