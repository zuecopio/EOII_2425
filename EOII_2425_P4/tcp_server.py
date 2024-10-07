"""
@file     tcp_server.py

@author   Marcos Belda Martinez <mbelmar@etsinf.upv.es>
@date     October, 2024
@section  EOII-GIIROB
@brief    TCP Server Code Implementation.
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
    This example creates a TCP socket and binds it to a specific IP address
    and port. It then receives a message from the client and sends a response.
    """
    # Create a TCP socket
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Set a timeout of 10 seconds
    tcp_socket.settimeout(10)
    
    # Define the port and IP address of the server to which we will connect
    server_address = ('localhost', 12000)

    # Server status variable
    server_on = True
    connection_on = False

    # Bind the socket object to the port and IP address
    tcp_socket.bind(server_address)

    # Put the server in listening mode to accept incoming connections
    tcp_socket.listen(1)
    
    while server_on == True:
        
        print("\n" + HEADER + "Waiting for incoming connections..." + RESET)
        
        # Accept an incoming connection ----------------------------------------
        try:
            connection, client_address = tcp_socket.accept()
            # Set a timeout of 10 seconds
            connection.settimeout(10)
            connection_on = True
            print(HEADER + "Connection established from:" + RESET, client_address)

        except socket.timeout:
            print(HEADER + "Error: Time for accepts has expired" + RESET)

        while connection_on == True:

            # Receive a message from client ------------------------------------
            try:
                data = connection.recv(4096)
                print(HEADER + "Message received from client:" + RESET, data.decode())
            
            except socket.timeout:
                print(HEADER + "Error: Data reception has expired" + RESET)
                connection_on = False

            except socket.error as err:
                print(f"{HEADER}Error receiving data: {err}{RESET}")
                connection_on = False

            if connection_on == True:

                # If client is closed do not send anything ---------------------
                if (data.decode()).lower() == "close client":
                    connection_on = False

                # If server has been asked to close, then say goodbye ----------
                elif ((data.decode()).lower() == "close server" or
                      (data.decode()).lower() == "close client and server"):
                    print(HEADER + "Goodbye!" + RESET)
                    connection_on = False
                    server_on = False

                # Send message using (pickle.dumps) ----------------------------
                elif (data.decode()).lower() == "request serialized message":
                    # Data to send (a list of numbers)
                    unserialized_msg = [1, 2, 3, 4, 5]
                    
                    # Serialize msg using pickle.dumps()
                    serialized_msg = pickle.dumps(unserialized_msg)
                    
                    # Send a response to client
                    print(HEADER + "Sending serialized message to client..." + RESET)
                    connection.send(serialized_msg)

                # Send message using (encode) ----------------------------------
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
                    connection.send(message.encode())
    
    # Close socket -------------------------------------------------------------
    connection.close()
    tcp_socket.close()
        
    ### end def __name__() ###

# end of file #
