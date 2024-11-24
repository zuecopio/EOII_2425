"""
@file     udp_client_class.py

@author   Marcos Belda Martinez <mbelmar@etsinf.upv.es>
@date     October, 2024
@section  EOII-GIIROB
@brief    UDP Client Class code implementation
          for using with tkinter UDP Client Window.
"""

# ---------------------------------------------------------------------------- #
# NEEDED IMPORTS

import json
import pickle
import socket
from   styles  import BUTTON_BG_COLOR
import threading
from   time    import sleep
import tkinter as tk

# ---------------------------------------------------------------------------- #
# CREATING UDP CLIENT CLASS

class udpClient(threading.Thread):
    
    def __init__(self, message_button, output_text, window):
        """
        Function to initialize UDP Client Class variables.
        The super() method is used to call the constructor of the parent class.
        """
        super().__init__() # Also: threading.Thread.__init__(self)
            
        # Control parameters
        self.client_on = True
        self.message2send = False
        self.message2recv = False

        # Variable to store the message
        self.clientMessage = ""

        # UDP Client Window elements needed in the class
        self.message_button = message_button
        self.output_text = output_text
        self.clientWindow = window
        
        # UDP Socket variables
        self.server_IP_address = None
        self.server_port = None

        # Create a UDP socket
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Set a timeout of 5 seconds
        self.udp_socket.settimeout(5)
        
        ### end def __init__() ###
    
    def setServerAddress(self, new_IP_address, new_port):
        """
        Function to set a new IP address and port for
        the server to which is wanted to send messages.
        """
        self.server_IP_address = new_IP_address
        self.server_port = new_port
            
        ### end def setServerAddress() ###
    
    def recieveMessage(self):
        """
        Function to recieve a message from server.
        """
        try:
            raw_data, server_adress = self.udp_socket.recvfrom(4096)
            
            # Case 1: waiting for a (pickle) type message ----------------------

            if (self.clientMessage).lower() == "request serialized message":
                # Deserialize the data using (pickle.loads)
                data = str(pickle.loads(raw_data))
            
            # Case 2: waiting for a (json) type message ------------------------

            elif ((self.clientMessage).lower() == 
                  "request json serialized message"):
                # Deserialize the data using (json.loads)
                jsonData = json.loads(raw_data)

                # Obtener la temperatura y la hora del mensaje
                temperature = str(jsonData["temperature"])
                timestamp = str(jsonData["timestamp"])

                # Imprimir los datos recibidos
                data = ("{Temperature: " + temperature +
                        "°C, Time: " + timestamp + "}")

            # Case 3: waiting for a (normal) type message ----------------------

            else:
                # Deserialize the data using (decode)
                data = raw_data.decode()

        except (socket.timeout, ConnectionResetError) as error:
            # If the server does not respond within 5
            # seconds, a warning will be sent
            data = "The server has not responded in 5 seconds"
            if isinstance(error, socket.timeout):
                data = "The server has not responded in 5 seconds"
            else:
                data = ("Connection error: The remote"
                        " host has closed the connection.")
        
        return data

        ### end def recieveMessage() ###

    def sendMessage(self, message):
        """
        Function to send a message to server.
        """
        self.clientMessage = message
        self.message2send = True

        if message.lower() != "end":
            self.message2recv = True
                
        ### end def sendMessage() ###

    def run(self):
        """
        This functions runs automatically when the thread is started.
        """
        while self.client_on == True:
            
            if self.message2send == True:

                if ((self.server_IP_address != None) and
                    (self.server_port != None)):
                    
                    # Send message to server
                    self.udp_socket.sendto(
                        self.clientMessage.encode(),
                        (self.server_IP_address, self.server_port))
                    
                    self.message2send = False

                    if (self.clientMessage).lower() == "end":
                        self.clientWindow.quit()
                        self.client_on = False

                    elif self.message2recv == True:

                        # Recieve confirmation answer from server
                        data = self.recieveMessage()

                        self.message2recv = False

                        # Check if client has been powered
                        # off during the timeout
                        if self.client_on == True:
                            self.output_text.insert(tk.END, data + "\n")
                            # Adjust scrollbar position to
                            # always show the last text
                            self.output_text.yview_moveto(1.0)

                            # Restore normal appearance of message button
                            self.message_button.config(
                                bg = BUTTON_BG_COLOR,
                                state = "normal",
                                text = "Send message")                       
                
            # Necessary wait to free the CPU
            sleep(0.001)

        ### end def run() ###

    def closeClient(self):
        """
        Function to close the client socket.
        """
        # Turn off the client
        self.client_on = False

        # Wait if a socket message is being expected
        while self.message2recv == True:
            sleep(0.001)

        # Close socket
        self.udp_socket.close()
            
        ### end def closeClient() ###
        
# end of file #