from Network import DroneNetwork
from function1 import check_reachability  # F1
from function2 import find_efficient_route  # F2
from function3 import calculate_max_flow  # F3
from function4 import find_critical_edges  # F4
from function6 import find_communication_network  # F6
import logging

# logging for tracking
logging.basicConfig(
    filename='drone_log.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

if __name__ == "__main__":
    network = DroneNetwork()
    logging.info("Program started")

    menu_text = """
DRONE NETWORK CONTROLLER
1. Load Network Data (JSON)
2. Add a Node
3. Add a Flight Path (Corridor)
4. Block a Flight Path
5. View Network Summary
6. [F1] Check Reachability
7. [F2] Find Efficient Route
8. [F3] Max Flow Analysis
9. [F4] Find Critical Edges
10. [F6] Communication Network (MST)
11. Exit
"""

    while True:
        try:
            print(menu_text)
            u_input = int(input("\nPlease make your choice: "))
            logging.info(f"user selected option: {u_input}")

            if u_input == 1:
                path = input("Enter file path (default: network_data.json): ") or "network_data.json"
                network.load_from_json(path)

            elif u_input == 2:
                network.add_node_menu()

            elif u_input == 3:
                network.add_corridor_menu()

            elif u_input == 4:
                network.block_edge()

            elif u_input == 5:
                network.print_summary()

            elif u_input == 6:
                start_node = input("Enter the hub id to start checking from (e.g., HUB1): ")
                check_reachability(network, start_node)

            elif u_input == 7:
                src = input("Enter start node id (e.g., HUB1): ")
                dst = input("Enter destination node id (e.g., HOUSE_A): ")
                req = input("Minimum required corridor capacity (default 1): ").strip()
                required_capacity = int(req) if req else 1
                find_efficient_route(network, src, dst, required_capacity)

            elif u_input == 8:
                src = input("Enter source hub id (e.g., HUB1): ")
                dst = input("Enter destination node id (e.g., HOUSE_A): ")
                calculate_max_flow(network, src, dst)

            elif u_input == 9:
                find_critical_edges(network)

            elif u_input == 10:
                find_communication_network(network)

            elif u_input == 11:
                print("Ending program")
                logging.info("Program ended")
                break

            else:
                print("Invalid selection")

            input("\nPress Enter to continue...")

        except ValueError:
            print("Please enter a valid number")
        except Exception as e:
            print(f"An error occurred: {e}")
            logging.error(f"Error: {e}")
