"""
@file     opc-ua_server.py

@author   Marcos Belda Martinez' <mbelmar@etsinf.upv.es>
@date     November, 2024
@section  EOII-GIIROB
@brief    OPC-UA Server Code Implementation.
"""

# ---------------------------------------------------------------------------- #
# NEEDED IMPORTS

from asyncua.sync import Server  # Import the synchronous Server class
import time  # For sleep function

# ---------------------------------------------------------------------------- #
# COLOR DEFINES

PURPLE = "\033[95m"  # Define purple color for console output
BOLD   = "\033[1m"   # Define bold text format
RESET  = "\033[0m"   # Define reset format for console output

# ---------------------------------------------------------------------------- #
# SERVER

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

    # Load definitions into the namespace
    server.start()  # Start the server
    time.sleep(30)  # Allow time for the server to initialize
    print("Creating new nodes...")  # Log message indicating node creation
    myobj = server.nodes.objects.add_object(idx, "MyObject")  # Add a new object
    myvar = myobj.add_variable(idx, "MyVariable", 6.7)  # Add a variable
   
    # Make the variable writable by clients
    myvar.set_writable()  
    
    # Start the client loop
    try:  
        count = 0  # Initialize counter
        while True:  
            time.sleep(1)  # Pause for 1 second

            # Read the value of the variable data
            value = myvar.read_value()  # Read the value
            print(BOLD + PURPLE + "(SERVER) " + RESET +
                  "The value of the data is: ", value)
            
            # do not modify the value
            """
            count += 0.1  # Increment the counter
            myvar.write_value(count)  # Write the updated value to the variable
            """           
            
    finally:  
        # Close the connection and clean up
        server.stop()  # Stop the server

# end of file #