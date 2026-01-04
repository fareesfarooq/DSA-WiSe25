# F2: Define No-Fly Zones (Basic Function)
# This function blocks specific flight paths (edges) between two nodes,
# making them no longer usable for drones.
def define_no_fly_zone(network):
    # Ask user for the start and end node of the flight path to block
    u = input("Enter start node ID to block: ")
    v = input("Enter end node ID to block: ")
    
    # Check if the edge exists between the nodes
    found = False
    for edge in network.adjacency[u]:
        if edge.to_node == v:
            # Block the edge if found
            edge.blocked = True
            found = True
            print(f"Path {u} -> {v} has been blocked (No-Fly Zone created).")
            break
    
    # If no such edge is found, notify the user
    if not found:
        print("Path not found, nothing was blocked.")
    
    # Optional: You can also block edges in the reverse direction for bidirectional edges
    if not found:
        for edge in network.adjacency[v]:
            if edge.to_node == u:
                edge.blocked = True
                found = True
                print(f"Path {v} -> {u} has been blocked (No-Fly Zone created).")
                break
    
    if not found:
        print("No valid flight corridor found between the specified nodes.")