from Network import DroneNetwork
from function2 import define_no_fly_zone
from function4 import find_critical_edges
from function1 import check_reachability  # For F1 (Check Reachability)
from function3 import calculate_max_flow  # For F3 (Max Flow)
from function6 import find_communication_network  # For F6 (Communication Infrastructure)
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
    
    # The menu text is defined here, but we print it inside the loop now
    menu_text = """
DRONE NETWORK CONTROLLER
1. Load Network Data (JSON)
2. Add a Node
3. Block a Flight Path
4. View Network Summary
5. [F1] Check Reachability
6. [F2] Define No-Fly Zone
7. [F3] Max Flow Analysis
8. [F4] Find Critical Edges
9. [F5] Minimum Maintenance Cost (MST)
10. [F6] Communication Network (MST)
11. Exit
"""
    
    while True:
        try:
            # Print the menu at the start of every loop
            print(menu_text)
            u_input = int(input("\nPlease make your choice: "))
            logging.info(f"user selected option: {u_input}")
            
            if u_input == 1:
                path = input("Enter file path (default: network_data.json): ") or "network_data.json"
                network.load_from_json(path)
            
            elif u_input == 2:
                network.add_node_menu()
            
            elif u_input == 3:
                network.block_edge()
            
            elif u_input == 4:
                network.print_summary()
            
            elif u_input == 5:
                start_node = input("Enter the hub id to start checking from (e.g., HUB1): ")
                check_reachability(network, start_node)  # F1: Check Reachability
            
            elif u_input == 6:
                define_no_fly_zone(network)  # F2: Define No-Fly Zone
            
            elif u_input == 7:
                # [F3] Max Flow Analysis
                src = input("Enter source hub id (e.g., HUB1): ")
                dst = input("Enter destination node id (e.g., HOUSE_A): ")
                calculate_max_flow(network, src, dst)  # F3: Max Flow Analysis
            
            elif u_input == 8:
                # F4: Find Critical Edges
                find_critical_edges(network)  # F4: Find Critical Edges
            
            elif u_input == 9:
                print("Function 5 goes here")  # F5 can be implemented here, or print a message for now
            
            elif u_input == 10:
                # F6: Communication Network (MST)
                find_communication_network(network)  # F6: Communication Network (MST)
                
            elif u_input == 11:
                print("Ending program")
                logging.info("Program ended")
                break

            else:
                print("Invalid selection")
            
            # Optional: Add a pause so the user can read the result before the menu clears/reappears
            input("\nPress Enter to continue...")
        
        except ValueError:
            print("Please enter a valid number")
        except Exception as e:
            print(f"An error occurred: {e}")
            logging.error(f"Error: {e}")
