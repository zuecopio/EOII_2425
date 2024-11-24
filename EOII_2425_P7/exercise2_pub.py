"""
@file     exercise2_pub.py

@author   Marcos Belda Martinez' <mbelmar@etsinf.upv.es>
@date     November, 2024
@section  EOII-GIIROB
@brief    Simulation of sensor data publishing using MQTT.
"""

# ---------------------------------------------------------------------------- #
# NEEDED IMPORTS

from   datetime import datetime  # For timestamping sensor data
import json                      # For JSON message formatting
import threading                 # For concurrent execution
import time                      # For sleep functionality
import paho.mqtt.client as mqtt  # MQTT client for messaging
import random                    # For generating random sensor values

# ---------------------------------------------------------------------------- #
# COLOR DEFINES

PURPLE = "\033[95m"  # Define purple color for console output
BOLD   = "\033[1m"   # Define bold text format
RESET  = "\033[0m"   # Define reset format for console output
HEADER = BOLD + PURPLE + "(PUBLISHER) " + RESET + PURPLE  # Header format

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
# PUBLISHER OBJECT CLASS

class Publisher(threading.Thread):

    def __init__(self, name):
        """
        Initialize the Publisher object with a name and set up connections.
        """
        super().__init__()  # Call the parent class constructor
        self.name = name  # Store the publisher's name

        # Assign random units of measurement for the sensor
        if (random.randrange(0, 2)):
            self.units = "F"  # Fahrenheit
        else:
            self.units = "C"  # Celsius

        # Configure MQTT publisher
        self.publisher = mqtt.Client(self.name)  # Create MQTT client
        self.publisher.connect(BROKER, PORT, 60)  # Connect to the broker
        print(HEADER + self.name + RESET + 
              " - Connected to broker (" + BROKER + ", " + str(PORT) + ")")
        self.publisher.loop_start()  # Start the MQTT loop

        ### end def __init__() ###
        
    def run(self):
        """
        Main loop for publishing sensor data.
        """
        while True:
            # Set random sensor value based on the sensor type
            if self.name == "sensor0":
                randTemp = random.randrange(-100, 101)  # Temperature range
            elif self.name == "sensor1":
                randTemp = random.randrange(0, 51)      # Temperature range
            elif self.name == "sensor2":
                randTemp = random.randrange(0, 5001)    # Temperature range

            # Get the current timestamp for the sensor reading
            current_time = datetime.now().time()
            date = current_time.strftime('%H:%M:%S')  # Format time

            # Generate JSON message with sensor data
            msg = {
                "Units": self.units,  # Measurement units
                "Value": randTemp,    # Sensor value
                "Time" : date         # Timestamp of the reading
            }

            # Publish the message to the corresponding MQTT topic
            self.publisher.publish(str(TOPICS[self.name]), json.dumps(msg))
            print(HEADER + self.name + RESET + 
                  " - New message sent via MQTT")  # Log message
            time.sleep(0.2)  # Sleep for a short duration

        ### end def run() ###

# ---------------------------------------------------------------------------- #
# MAIN FUNCTION

if __name__ == '__main__':
    """
    Main entry point for the program. Determines if the file is run as a 
    script or imported as a module.
    """
    
    # CREATING PUBLISHER THREADS

    publishers = [
        Publisher("sensor0"),  # Create publisher for sensor0
        Publisher("sensor1"),  # Create publisher for sensor1
        Publisher("sensor2")   # Create publisher for sensor2
    ]

    # STARTING PUBLISHER THREADS

    for publisher in publishers:
        publisher.start()  # Start each publisher thread

    # WAIT UNTIL ALL PUBLISHERS FINISH

    for publisher in publishers:
        publisher.join()  # Wait for each publisher to finish

# end of file #