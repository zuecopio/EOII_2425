"""
@file     opc-ua_client_robots.py

@author   Marcos Belda Martinez' <mbelmar@etsinf.upv.es>
@date     November, 2024
@section  EOII-GIIROB
@brief    Implementing OPC-UA Robot Data Client Code.
"""

# ---------------------------------------------------------------------------- #
# NEEDED IMPORTS

from asyncua.sync import Client   # Import the synchronous Client class
import random # For generating random values
import time   # For sleep function

# ---------------------------------------------------------------------------- #
# COLOR DEFINES

YELLOW = "\033[93m"  # Define yellow color for console output
BOLD   = "\033[1m"   # Define bold text format
RESET  = "\033[0m"   # Define reset format for console output

# ---------------------------------------------------------------------------- #
# FUNCTION TO UPDATE ROBOT POSITION

def update_robot_position(client, robot_id, robot_number,
                          pos_x_node, pos_y_node, min_pos, max_pos):
    """
    Updates the position of a robot by reading, modifying, and setting 
    new values for its X and Y coordinates.
    """
    # Read the current X position from the node
    pos = pos_x_node.read_value()

    # Check if the position is within the defined range
    if min_pos <= pos < max_pos:
        pos += 1  # Increment position if within range
    else:
        pos = min_pos  # Reset to minimum position if out of range
    
    # Print the updated coordinates for the robot
    print(BOLD + YELLOW + "(CLIENT) " + RESET +
          f"Coordinates of Robot {robot_number}: ({pos}, {pos})")
    
    # Set the new X and Y position values in the nodes
    pos_x_node.set_value(pos)
    pos_y_node.set_value(pos)

    ### end def update_robot_position() ###

# ---------------------------------------------------------------------------- #
# CLIENT

if __name__ == "__main__":
    """
    Main entry point for the OPC UA client application.
    """  
    with Client("opc.tcp://localhost:4840/freeopcua/server/") as client:  
        
        # Access the specific variable by navigating the node hierarchy
        robots = {
            1: (client.nodes.root.get_child(
                    ["0:Objects", "1:Robot1", "1:R1Pos_x"]),
                client.nodes.root.get_child(
                    ["0:Objects", "1:Robot1", "1:R1Pos_y"]),
                0, 200),
            
            2: (client.nodes.root.get_child(
                    ["0:Objects", "2:Robot2", "2:R2Pos_x"]),
                client.nodes.root.get_child(
                    ["0:Objects", "2:Robot2", "2:R2Pos_y"]),
                201, 400),
            
            3: (client.nodes.root.get_child(
                    ["0:Objects", "3:Robot3", "3:R3Pos_x"]),
                client.nodes.root.get_child(
                    ["0:Objects", "3:Robot3", "3:R3Pos_y"]),
                401, 600),
        }

        while True:
            time.sleep(0.5)  # Pause for 0.5 second
            
            for robot_number, (pos_x_node, pos_y_node,
                               min_pos, max_pos) in robots.items():
                update_robot_position(client, robot_number, robot_number,
                                      pos_x_node, pos_y_node, min_pos, max_pos)

# end of file #