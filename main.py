from Network import DroneNetwork
from function1 import check_reachability
from function3 import calculate_max_flow 
import logging

# logging for tracking
logging.basicConfig(
    filename='drone_log.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

if __name__ == "__main__":
    network = DroneNetwork()
    logging.info("program started")

    # The menu text is defined here, but we print it inside the loop now
    menu_text = """
                                  DRONE NETWORK CONTROLLER

                    1.            Load Network Data (JSON)
                    2.                  Add a Node
                    3.                 Block a Flight Path
                    4.               View Network Summary
                    5.              [F1] Check Reachability
                    6.                  [F2] Shortest Path
                    7.              [F3] Max Flow Analysis
                    8.                [F4] Find Critical Edges
                    9.         [F5] Minimum Maintenance Cost (MST)
                    10.         [F6]        Function 6
                    11.                          Exit
    """

    while True:
        try:
            # Print the menu at the start of every loop
            print(menu_text)

            u_input = int(input("\nplease make your choice: "))
            logging.info(f"user selected option: {u_input}")

            if u_input == 1:
                path = input(
                    "enter file path (default: network_data.json): "
                ) or "network_data.json"
                network.load_from_json(path)

            elif u_input == 2:
               
                network.add_node_menu()

            elif u_input == 3:
                
                network.block_edge()

            elif u_input == 4:
                
                network.print_summary()

            elif u_input == 5:
                
                start_node = input(
                    "enter the hub id to start checking from (e.g., HUB1): ")
                check_reachability(network, start_node)

            elif u_input == 6:
               
                print("Function 2 goes here")

            elif u_input == 7:
                # [F3] Max Flow Analysis
                src = input("enter source hub id (e.g., HUB1): ")
                dst = input("enter destination node id (e.g., HOUSE_A): ")
                calculate_max_flow(network, src, dst)

            elif u_input == 8:
                print("Function 4 goes here")

            elif u_input == 9:
                print("Function 5 goes here")

            elif u_input == 10:
                print("Function 6 goes here")

            elif u_input == 11:
                print("ending program")
                logging.info("program ended")
                break

            else:
                print("invalid selection")

            # Optional: Add a pause so the user can read the result before the menu clears/reappears
            input("\nPress Enter to continue...")

        except ValueError:
            print("please enter a valid number")

        except Exception as e:
            print(f"an error occured: {e}")
            logging.error(f"error: {e}")
