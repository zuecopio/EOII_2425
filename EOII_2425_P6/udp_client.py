"""
@file     udp_client.py

@author   Marcos Belda Martinez' <mbelmar@etsinf.upv.es>
@date     November, 2024
@section  EOII-GIIROB
@brief    UDP Client Code Implementation (sending messages in a loop).
"""

# ---------------------------------------------------------------------------- #
# NEEDED IMPORTS

import socket           # Import socket for UDP communication
from time import sleep  # Import sleep for timing control

# ---------------------------------------------------------------------------- #
# COLOR DEFINES

PURPLE = "\033[95m"  # Define purple color for console output
BOLD   = "\033[1m"   # Define bold text format
RESET  = "\033[0m"   # Define reset format for console output
HEADER = BOLD + PURPLE + "(CLIENT) " + RESET + PURPLE  # Header format

# ---------------------------------------------------------------------------- #
# CLIENT

if __name__ == '__main__':
    """
    This example creates a UDP socket and
    uses it to send a message to the server.
    """
    # Create a UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Get the server's IP address and port
    server_address = ('localhost', 2999)
    
    # Set a timeout of 5 seconds
    udp_socket.settimeout(5)

    # Initialize the value of the variable to be sent to the server
    variable = 0

    # Client status variable
    client_on = True
    
    # Loop to send messages until the client is closed
    while client_on == True:
        
        # Send the current variable value as a message to the server
        print(HEADER + "Sending message to server: " + RESET + str(variable))  
        udp_socket.sendto(str(variable).encode(), server_address)
        
        # Update the variable value for the next message
        if variable < 100:
            variable += 1  # Increment variable
        else:
            variable = 0  # Reset variable to 0

        # Pause for 0.5 seconds before sending the next message
        sleep(0.500)

    # Close the UDP socket when done
    udp_socket.close()

# end of file #