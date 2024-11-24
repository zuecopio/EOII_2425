"""
@file     tcp_client.py

@author   Marcos Belda Martinez' <mbelmar@etsinf.upv.es>
@date     October, 2024
@section  EOII-GIIROB
@brief    TCP Client Code Implementation.
"""

# ---------------------------------------------------------------------------- #
# NEEDED IMPORTS

import pickle           # For serializing and deserializing Python objects
import socket           # For network communication using sockets
from time import sleep  # For adding delays in execution

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
    This example creates a TCP socket and uses it to send a message to
    the server. It then receives a response from the server and prints it.
    """
    # Create a TCP socket
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Set a timeout of 5 seconds
    tcp_socket.settimeout(5)

    # Define the port and IP address of the server to which we will connect
    server_address = ('localhost', 12000)

    # Client status variable
    connection_on = False

    # Establish a connection to the server
    try:
        tcp_socket.connect(server_address)
        connection_on = True
        # Help menu
        print(HEADER + "Available options to interact with the server:" + RESET)
        print(" - 'TIME'")
        print(" - 'REQUEST SERIALIZED MESSAGE'")
        print(" - 'CLOSE CLIENT'")
        print(" - 'CLOSE SERVER'")
        print(" - 'CLOSE CLIENT AND SERVER'\n")
        sleep(0.001) # aesthetic sleep for execution in the same terminal

    except socket.timeout:
        print(HEADER + "Error: The connection has expired" + RESET)
        client_on = False

    except socket.error as err:
        print(f"{HEADER}Connection error: {err}{RESET}")
        client_on = False

    # Read and send messages until the client is asked to close
    while connection_on == True:
        
        # Read message from keyboard input -------------------------------------
        message = input(HEADER + "Write a message: " + RESET)
        
        # Analyze, send and recieve messages -----------------------------------
        try:
            
            # Closing requests -------------------------------------------------
            if (message.lower() == "close client" or
                message.lower() == "close server" or
                message.lower() == "close client and server"):
                print(HEADER + "Notifying server..." + RESET)
                tcp_socket.send(message.encode())
                connection_on = False

                if "server" in message.lower():
                    print(HEADER + "Now server is closed, unable to send messages" + RESET)
            
                print(HEADER + "Goodbye!" + RESET)
                       
            # Send normal message to server ------------------------------------
            else:
                print(HEADER + "Sending message to server..." + RESET)
                tcp_socket.send(message.encode())
                
                # Receive a response from server -------------------------------
                # (max data buffer size: 4096)
                data = tcp_socket.recv(4096)
                
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
    tcp_socket.close()

# end of file #