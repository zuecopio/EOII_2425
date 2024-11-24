"""
@file     exercise2_sub.py

@author   Marcos Belda Martinez' <mbelmar@etsinf.upv.es>
@date     November, 2024
@section  EOII-GIIROB
@brief    Basic sensors simulation for data handling.
"""

# ---------------------------------------------------------------------------- #
# NEEDED IMPORTS

import threading                 # Import threading for concurrent execution
import paho.mqtt.client as mqtt  # Import MQTT client for messaging
import socket                    # Import socket for UDP communication

# ---------------------------------------------------------------------------- #
# COLOR DEFINES

YELLOW = "\033[93m"  # Define yellow color for console output
BOLD   = "\033[1m"   # Define bold text format
RESET  = "\033[0m"   # Define reset format for console output
HEADER = BOLD + YELLOW + "(SUBSCRIBER) " + RESET + YELLOW  # Header format

# ---------------------------------------------------------------------------- #
# PARAMETERS AND TOPICS FOR UDP CONNECTION WITH SERVER

SERVER_IP_ADDRESS = "localhost"  # IP address of the UDP server
PORTS = {  # Define ports for each sensor
    "sensor0": 3000,
    "sensor1": 3001,
    "sensor2": 3002
}

# ---------------------------------------------------------------------------- #
# PARAMETERS AND TOPICS FOR CONNECTION WITH MQTT

BROKER = "localhost"  # MQTT broker address
PORT   = 1883  # MQTT broker port number
TOPICS = {  # Define MQTT topics for each sensor
    "sensor0": "sensors/sensor0/data",
    "sensor1": "sensors/sensor1/data",
    "sensor2": "sensors/sensor2/data"
}

# ---------------------------------------------------------------------------- #
# CLIENT OBJECT CLASS

class Client(threading.Thread):

    def __init__(self, name):
        """
        Initialize the Client object with a name and set up connections.
        """
        super().__init__()  # Call the parent class constructor
        self.name = name  # Store the client's name
        
        # Create a UDP socket for communication
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Set a timeout of 5 seconds for the UDP socket
        self.udp_socket.settimeout(5)

        # Configure MQTT subscriber
        self.client = mqtt.Client(self.name + "_sub")  # Create MQTT client
        self.client.connect(BROKER, PORT, 60)  # Connect to the MQTT broker
        print(HEADER + self.name + RESET + 
              " - Connected to broker (" + BROKER + ", " + str(PORT) + ")")
        self.client.on_connect = self.on_connect  # Set connect callback
        self.client.on_message = self.on_message  # Set message callback
        self.client.loop_start()  # Start the MQTT loop

        ### end def __init__() ###

    def on_connect(self, client, userdata, flags, rc):
        """
        Callback for when the client connects to the MQTT broker.
        """
        # Subscribe to the topic corresponding to this client
        self.client.subscribe(TOPICS[self.name])
        print(HEADER + self.name + RESET + 
              " - Successfully subscribed to \"" +
              TOPICS[self.name] + "\" topic")

        ### end def on_connect() ###
        
    def on_message(self, client, userdata, message):
        """
        Callback for when a message is received from the MQTT broker.
        """
        print(HEADER + self.name + RESET + 
              " - Message received via MQTT and sent to port (" +
              str(PORTS[self.name]) + ") via UDP")
        
        # Check if the message topic matches the client's topic
        if (message.topic == TOPICS[self.name]):
            # Send the message payload to the server via UDP
            self.udp_socket.sendto(
                message.payload,
                (SERVER_IP_ADDRESS, PORTS[self.name]))

        ### end def on_message() ###
        
    def run(self):
        """
        The main loop for the client thread.
        """
        while True:
            pass  # Keep the thread alive

        ### end def run() ###

# ---------------------------------------------------------------------------- #
# MAIN FUNCTION

if __name__ == '__main__':
    """
    Main entry point for the program. Determines if the file is run as a 
    script or imported as a module.
    """
    
    # CREATING CLIENT THREADS

    clients = [
        Client("sensor0"),  # Create client for sensor0
        Client("sensor1"),  # Create client for sensor1
        Client("sensor2")   # Create client for sensor2
    ]

    # STARTING CLIENT THREADS

    for client in clients:
        client.start()  # Start each client thread

    # WAIT UNTIL ALL CLIENTS FINISH

    for client in clients:
        client.join()  # Wait for each client to finish
        
# end of file #