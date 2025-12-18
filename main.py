from Network import DroneNetwork
import logging

# logging for tracking
logging.basicConfig(
    filename='drone_log.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

if __name__ == "__main__":
    network = DroneNetwork()

    menu_text = """
                                  DRONE NETWORK CONTROLLER

                    1.            Load Network Data (JSON)
                    2.               View Menu Options
                    3.                  Add a Node
                    4.                 Block a Flight Path
                    5.          View network summary
                    6.              [F1] Check Reachability
                    7.                  [F2] Shortest Path
                    8.              [F3] Max Flow Analysis
                    9.                [F4] Find Critical Edges
                    10.         [F5] Minimum Maintenance Cost (MST)
                    11.         [F6]        Function 6
                    12.                          Exit
    """

    print(menu_text)
    logging.info("program started")

    while True:
        try:
            u_input = int(input("\nplease make your choice: "))
            logging.info(f"user selected option: {u_input}")

            if u_input == 1:
                path = input(
                    "enter file path (default: network_data.json): "
                ) or "network_data.json"
                network.load_from_json(path)

            elif u_input == 2:
                print(menu_text)

            elif u_input == 3:
                network.add_node_menu()

            elif u_input == 4:
                network.block_edge()

            elif u_input == 5:
                network.print_summary()

            elif u_input == 6:
                print("Function 1 goes here")

            elif u_input == 7:
                print("Function 2 goes here")

            elif u_input == 8:
                print("Function 3 goes here")

            elif u_input == 9:
                print("Function 4 goes here")

            elif u_input == 10:
                print("Function 5 goes here")

            elif u_input==11:
                print("Function 6 goes here")

            elif u_input == 12:
                print("ending program")
                logging.info("program ended")
                break

            else:
                print("invalid selection")

        except ValueError:
            print("please enter a valid number")

        except Exception as e:
            print(f"an error occured: {e}")
            logging.error(f"error: {e}")
