"""
@file     client.py

@author   Marcos Belda Martinez <mbelmar@etsinf.upv.es>
@date     September, 2024
@section  EOII-GIIROB
@brief    UDP Client Code Implementation.
"""

# ---------------------------------------------------------------------------- #
# NEEDED IMPORTS

import socket
import pickle

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
       
    while True:
        
        message = input(HEADER + "Write a message: " + RESET)
        if message == "END":
            print(HEADER + "Goodbye!" + RESET)
            break
        
        # Send a message to server (encode converts to bytes)
        print(HEADER + "Sending message to server..." + RESET)
        udp_socket.sendto(message.encode(), server_address)
        
        try:
            # Receive a response from server
            # (max data buffer size: 4096)
            data, server_adress = udp_socket.recvfrom(4096)
            
            full_message = HEADER + "Message received from server: " + RESET
            
            if message == "request serialized message":
                # Deserialize the data using pickle.loads()
                print(full_message + (str)(pickle.loads(data)))
            else:
                print(full_message + data.decode())
        
        except socket.timeout:
            # If the server does not respond within 5 seconds, a message is printed
            print(HEADER + "The server has not responded in 5 seconds" + RESET)
    
    # Close socket
    udp_socket.close()
        
    ### end def __name__() ###

# end of file #