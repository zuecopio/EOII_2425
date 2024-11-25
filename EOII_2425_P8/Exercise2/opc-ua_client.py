"""
@file     opc-ua_client.py

@author   Marcos Belda Martinez' <mbelmar@etsinf.upv.es>
@date     November, 2024
@section  EOII-GIIROB
@brief    OPC-UA Client Code Implementation.
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
# CLIENT

if __name__ == "__main__":
    """
    Main entry point for the OPC UA client application.
    """  
    with Client("opc.tcp://localhost:4840/freeopcua/server/") as client:  
        
        # Access the specific variable by navigating the node hierarchy
        myvar = client.nodes.root.get_child(
            ["0:Objects", "2:MyObject", "2:MyVariable"])  

        while True:
            
            time.sleep(1)  # Pause for 1 second

            # Get a random value between -100.0 and 100.0
            value = random.uniform(-100.0, 101.0)

            # Write a new value to the variable 
            print(BOLD + YELLOW + "(CLIENT) " + RESET +
                  "Modifying data value to...", value)   
            myvar.set_value(value)  # Update the variable's value
        
        # Do not delete. This is the original code example
        """
        # Retrieve all child nodes from the root node
        obj_space = client.nodes.root.get_children()  
        print(BOLD + YELLOW + "(PRINT 1) " + RESET +
            "The children from the root are: ", obj_space)  

        # Access the specific variable by navigating the node hierarchy
        myvar = client.nodes.root.get_child(
        ["0:Objects", "2:MyObject", "2:MyVariable"])  

        # Read the data value of the variable
        result1 = myvar.read_data_value()  # Read the value
        print(BOLD + YELLOW + "(PRINT 2) " + RESET +
            "The value of the data is: ", result1)  

        # Read the value using Python's built-in method
        result2 = myvar.read_value()  
        print(BOLD + YELLOW + "(PRINT 3) " + RESET +
            "The value before writing is: ", result2)  

        # Write a new value to the variable
        myvar.set_value(1000.9)  # Update the variable's value  

        # Read the value again to confirm the update
        result3 = myvar.read_value()   
        print(BOLD + YELLOW + "(PRINT 4) " + RESET +
            "The value after writing is: ", result3)  

        # Retrieve the object node for further operations
        obj = client.nodes.root.get_child(["0:Objects", "2:MyObject"])  
        print(BOLD + YELLOW + "(PRINT 5) " + RESET +
            "myobj is: ", obj)  # Print the retrieved object
        """

# end of file #