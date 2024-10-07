"""
@file     udp_server.py

@author   Marcos Belda Martinez <mbelmar@etsinf.upv.es>
@date     September, 2024
@section  EOII-GIIROB
@brief    UDP Server Code Implementation.
"""

# ---------------------------------------------------------------------------- #
# NEEDED IMPORTS

from datetime import datetime
import pickle
import socket

# ---------------------------------------------------------------------------- #
# COLOR DEFINES

YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"
HEADER = BOLD + YELLOW + "(SERVER) " + RESET + YELLOW

# ---------------------------------------------------------------------------- #
# SERVER

if __name__ == '__main__':
    """
    This example creates a UDP socket and binds it to a specific IP address
    and port. It then receives a message from the client and sends a response.
    """
    # Create a UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Get the server's IP address and port
    server_address = ('localhost', 12000)
    
    # Bind the socket to the server address and port
    udp_socket.bind(server_address)

    # Server status variable
    server_on = True
    
    while server_on:
        
        # Receive a message from client ----------------------------------------
        data, client_address = udp_socket.recvfrom(4096)
        print(HEADER + "Message received from client:" + RESET, data.decode())
        
        # If client is closed do not send anything -----------------------------
        if (data.decode()).lower() == "close client":
            pass

        # If server has been asked to close, then say goodbye ------------------
        elif ((data.decode()).lower() == "close server" or
              (data.decode()).lower() == "close client and server"):
            print(HEADER + "Goodbye!" + RESET)
            server_on = False

        # Send message using (pickle.dumps) ------------------------------------
        elif (data.decode()).lower() == "request serialized message":
            # Data to send (a list of numbers)
            unserialized_msg = [1, 2, 3, 4, 5]
            
            # Serialize msg using pickle.dumps()
            serialized_msg = pickle.dumps(unserialized_msg)
            
            # Send a response to client
            print(HEADER + "Sending serialized message to client..." + RESET)
            udp_socket.sendto(serialized_msg, client_address)
        
        # Send message using (encode) ------------------------------------------
        else:
            if (data.decode()).lower() == "time":
                # Get the current time
                current_time = datetime.now().time()
                # Convert the current time to a string in the format hh:mm:ss
                message = current_time.strftime('%H:%M:%S')       
            else:
                message = "Nothing to say"
            
            # Send a response to client
            print(HEADER + "Sending message to client..." + RESET)
            udp_socket.sendto(message.encode(), client_address)
    
    # Close socket -------------------------------------------------------------
    udp_socket.close()
        
    ### end def __name__() ###

# end of file #
