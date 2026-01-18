# Drone Network Planning Tool (DSA Project)

This project was developed for the **Algorithms and Data Structures WiSe 25/26** course.  
It implements a planning and analysis tool for an autonomous drone delivery network using classical graph algorithms.

The city is modelled as a graph where nodes represent locations (distribution hubs, delivery points, charging stations) and edges represent flight corridors with energy costs and capacity constraints.

---

## Features

- Load a drone network from a JSON file
- Add and modify nodes in the network
- Block flight corridors (no-fly zones)
- Check reachability of all delivery points (BFS)
- Compute energy-efficient routes (Dijkstra)
- Calculate delivery capacity using Max Flow (Edmonds–Karp)
- Identify critical connections in the network
- Build a minimum-cost communication network (MST / Prim)

---

## Project Structure

- `Network.py` – Graph data structure (nodes, edges, adjacency list)
- `main.py` – Menu-driven controller
- `function1.py` – Reachability check (BFS)
- `function2.py` – Efficient routing (Dijkstra)
- `function3.py` – Delivery capacity (Max Flow)
- `function4.py` – Network resilience
- `function6.py` – Communication infrastructure (MST)
- `network_data.json` – Example input network

## Authors:
## Farees Farooq Ismail
## Hussain Ahmed