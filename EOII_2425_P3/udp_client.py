"""
@file     udp_client.py

@author   Marcos Belda Martinez <mbelmar@etsinf.upv.es>
@date     September, 2024
@section  EOII-GIIROB
@brief    UDP Client Code Implementation.
"""

# ---------------------------------------------------------------------------- #
# NEEDED IMPORTS

import pickle
import socket
from time import sleep

# ---------------------------------------------------------------------------- #
# COLOR DEFINES

PURPLE = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"
HEADER = BOLD + PURPLE + "(CLIENT) " + RESET + PURPLE

# ---------------------------------------------------------------------------- #
# CLIENT

if __name__ == '__main__':
    """
    This example creates a UDP socket and uses it to send a message to
    the server. It then receives a response from the server and prints it.
    """
    # Create a UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Get the server's IP address and port
    server_address = ('localhost', 12000)
    
    # Set a timeout of 5 seconds
    udp_socket.settimeout(5)

    # Client status variable
    client_on = True
    
    # Read and send messages until the client is asked to close
    while client_on == True:
        
        # Read message from keyboard input -------------------------------------
        message = input(HEADER + "Write a message: " + RESET)
        
        # Analyze, send and recieve messages -----------------------------------
        try:
            
            # Closing requests -------------------------------------------------
            if (message.lower() == "close client" or
                message.lower() == "close server" or
                message.lower() == "close client and server"):
                if "server" in message.lower():
                    udp_socket.sendto(message.encode(), server_address)
                    sleep(0.001)
                
                if "client" in message.lower():
                    print(HEADER + "Goodbye!" + RESET)
                    client_on = False
            
            # Send normal message to server ------------------------------------
            else:
                print(HEADER + "Sending message to server..." + RESET)
                udp_socket.sendto(message.encode(), server_address)
                
                # Receive a response from server -------------------------------
                # (max data buffer size: 4096)
                data, server_adress = udp_socket.recvfrom(4096)
                
                full_message = HEADER + "Message received from server: " + RESET
                
                if (message).lower() == "request serialized message":
                    # Deserialize the data using (pickle.loads)
                    print(full_message + (str)(pickle.loads(data)))
                else:
                    # Deserialize the data using (decode)
                    print(full_message + data.decode())
        
        except socket.timeout:
            # If the server does not respond within 5 seconds, a message is printed
            print(HEADER + "The server has not responded in 5 seconds" + RESET)

    # Close socket -------------------------------------------------------------
    udp_socket.close()
        
    ### end def __name__() ###

# end of file #