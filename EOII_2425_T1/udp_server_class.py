"""
@file     udp_server_class.py

@author   Marcos Belda Martinez' <mbelmar@etsinf.upv.es>
@date     October, 2024
@section  EOII-GIIROB
@brief    UDP Server Class code implementation
          for using with tkinter UDP Server Window.
"""

# ---------------------------------------------------------------------------- #
# NEEDED IMPORTS

from   datetime import datetime
import json
import pickle
import socket
import threading
from   time    import sleep
import tkinter as tk

# ---------------------------------------------------------------------------- #
# CREATING UDP CLIENT CLASS

class udpServer(threading.Thread):
    
    def __init__(self, checkbuttons, output_text, serverWindow):
        """
        Function to initialize UDP Server Class variables.
        The super() method is used to call the constructor of the parent class.
        """
        super().__init__() # Also: threading.Thread.__init__(self)
            
        # Control parameters
        self.server_on = False
        self.recievingMessage = False

        
        # UDP Server Window elements needed in the class
        self.checkbuttons = checkbuttons
        self.output_text = output_text
        self.serverWindow = serverWindow

        # UDP Socket variables
        self.server_IP_address = "localhost"
        self.server_port = None

        # Create a UDP socket
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Set a timeout of 1 seconds
        self.udp_socket.settimeout(1)
        
        ### end def __init__() ###
    
    def setServerPort(self, new_port):
        """
        Function to set a new server port.
        """
        self.server_port = new_port
            
        ### end def setServerPort() ###

    def showClientMessage(self, data):
        """
        Show client message on output_text
        (depending on checkbuttons values).
        """
        if self.checkbuttons["check_uppercase"].get() == True:
            message = data.upper()

        elif self.checkbuttons["check_lowercase"].get() == True:
            message = data.lower()

        elif self.checkbuttons["check_count"].get() == True:
            # Initialize counters
            num_letters    = 0
            num_vowels     = 0
            num_consonants = 0

            # Define vowels
            vowels = "aeiouAEIOU"

            # Iterate through each character in the text
            for char in data:
                if char.isalpha():  # Check if it is a letter
                    num_letters += 1
                    
                    if char in vowels:  # Check if it is a vowel
                        num_vowels += 1
                    else:  # If not, then it is a consonant
                        num_consonants += 1
            
            message = ("Letters: "      + str(num_letters) +
                       ", Vowels: "     + str(num_vowels)  +
                       ", Consonants: " + str(num_consonants))
        
        else:
            message = data

        self.output_text.insert(tk.END, message + "\n")
        # Adjust scrollbar position to always show the last text
        self.output_text.yview_moveto(1.0)
              
        ### end def showClientMessage() ###
    
    def run(self):
        """
        This functions runs automatically when the thread is started.
        """
        # Bind the socket to the server address and port
        self.udp_socket.bind((self.server_IP_address, self.server_port))

        # Server status variable
        self.server_on = True

        while self.server_on == True:
            
            # Receive a message from client ------------------------------------
            self.recievingMessage = True
            try:
                data, client_address = self.udp_socket.recvfrom(4096)
                self.showClientMessage(data.decode())

            except (socket.timeout, RuntimeError):
                # socket.timeout: when the timeout period expires
                # RuntimeError: when main thread is not in main loop
                data = None
            
            self.recievingMessage = False
            
            if data != None:
                    
                # If server has been asked to close, then say goodbye ----------
                if (data.decode()).lower() == "end":
                    self.server_on = False
                    self.serverWindow.quit()

                # Send message using (pickle.dumps) ----------------------------
                elif (data.decode()).lower() == "request serialized message":
                    # Data to send (a list of numbers)
                    unserialized_msg = [1, 2, 3, 4, 5]
                    
                    # Serialize msg using pickle.dumps()
                    serialized_msg = pickle.dumps(unserialized_msg)
                    
                    # Send a response to client
                    self.udp_socket.sendto(serialized_msg, client_address)
                
                # Send message using (json.dumps) ------------------------------
                elif ((data.decode()).lower() ==
                      "request json serialized message"):
                    # Create the message in JSON format
                    unserialized_msg = {
                        "temperature": 22,
                        "timestamp": (datetime.now()
                                      .strftime("%Y-%m-%d %H:%M:%S"))
                    }
                    
                    # Serialize msg using json.dumps()
                    serialized_msg = json.dumps(unserialized_msg)
                    
                    # Send a response to client
                    self.udp_socket.sendto(
                        serialized_msg.encode(), 
                        client_address)
                
                # Send message using (encode) ----------------------------------
                else:
                    if (data.decode()).lower() == "time":
                        # Get the current time
                        current_time = datetime.now().time()
                        # Convert the current time to a
                        # string in the format hh:mm:ss
                        message = current_time.strftime('%H:%M:%S')       
                    else:
                        message = "Nothing to say"
                    
                    # Send a response to client
                    self.udp_socket.sendto(message.encode(), client_address)
                
            # Necessary wait to free the CPU
            sleep(0.001)
        
        ### end def run() ###

    def closeClient(self):
        """
        Function to close the client socket.
        """
        # Turn off the server
        self.server_on = False

        # Wait if a socket message is being expected
        while self.recievingMessage == True:
            sleep(0.001)

        # Close socket
        self.udp_socket.close()
            
        ### end def closeClient() ###
        
# end of file #