"""
@file     opc-ua_server.py

@author   Marcos Belda Martinez' <mbelmar@etsinf.upv.es>
@date     November, 2024
@section  EOII-GIIROB
@brief    Implementing OPC-UA Robot Data Server Code.
"""

# ---------------------------------------------------------------------------- #
# NEEDED IMPORTS

from asyncua.sync import Server  # Import the synchronous Server class
from asyncua import ua # Import the ua module for OPC UA data types and methods
import time  # For sleep function

# ---------------------------------------------------------------------------- #
# COLOR DEFINES

PURPLE = "\033[95m"  # Define purple color for console output
BOLD   = "\033[1m"   # Define bold text format
RESET  = "\033[0m"   # Define reset format for console output

# ---------------------------------------------------------------------------- #
# SERVER

def create_robot(server, idx, robot_name, posx_name, posy_name):
    """
    Creates a robot object and its position variables in the server.
    """
    myobj = server.nodes.objects.add_object(idx, robot_name)  
    myrob_posx = myobj.add_variable(idx, posx_name, 0)  
    myrob_posy = myobj.add_variable(idx, posy_name, 0)

    # Give write permission to variables
    myrob_posx.set_writable()  
    myrob_posy.set_writable()
    
    return myrob_posx, myrob_posy

    ### end def create_robot() ###

def read_robot_coordinates(robot_id, posx, posy):
    """
    Reads and prints the coordinates of a robot.
    """
    valueX = posx.read_value()  # Read the value
    valueY = posy.read_value()  # Read the value
    print(BOLD + PURPLE + "(SERVER) " + RESET +
          f"{robot_id} coordinates: ({valueX}, {valueY})")
    
    ### end def read_robot_coordinates() ###

if __name__ == '__main__':
    """
    Main entry point for the OPC UA server application.
    """
    # Start the OPC UA server
    server = Server()  
    server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")  

    # Create a namespace; not strictly necessary, but useful for organization
    uri = "http://localhost/mynamespace"  
    idx = server.register_namespace(uri)  # Register the namespace
    print(BOLD + PURPLE + "(SERVER) " + RESET +
          f"Registered namespace: {uri} with index: {idx}")  

    # Define robots and their position variable names
    robots = [
        ("Robot1", "R1Pos_x", "R1Pos_y"),
        ("Robot2", "R2Pos_x", "R2Pos_y"),
        ("Robot3", "R3Pos_x", "R3Pos_y")
    ]

    # Populate the address space and create variables for each robot
    robot_variables = {}
    for idx, (robot_name, posx_name, posy_name) in enumerate(robots, start=1):
        robot_variables[robot_name] = create_robot(server, idx, robot_name,
                                                   posx_name, posy_name)

    # Start the OPC UA server
    server.start()

    # Start the server loop  
    try:  
        while True:  
            time.sleep(0.5)  # Pause for 0.5 second between updates

            # Read and print coordinates for each robot
            for robot_name, (posx, posy) in robot_variables.items():
                read_robot_coordinates(robot_name, posx, posy)

    finally:  
        # Close the connection and clean up
        server.stop()  # Stop the server

# end of file #