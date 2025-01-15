"""
@file     opc-ua_server.py

@author   Marcos Belda Martinez' <mbelmar@etsinf.upv.es>
@date     January, 2025
@section  EOII-GIIROB
@brief    OPC-UA Server & MQTT Subscriber Code Implementation.
"""

# ---------------------------------------------------------------------------- #
# NEEDED IMPORTS

import json                          # For handling JSON data
import logging                       # For logging messages
import sys                           # For using exit() function
import threading                     # For concurrent execution of threads
from time import sleep               # For sleep function

import paho.mqtt.client as mqtt      # For MQTT communication
from asyncua.sync import Server, ua  # Import the synchronous Server class

# ---------------------------------------------------------------------------- #
# LOGGER CONFIGURATION

# Basic logger configuration
logging.basicConfig(
    level = logging.DEBUG
    , format = '%(asctime)s - %(name)s - %(levelname)s'
               ' - %(funcName)s - %(message)s'
    , datefmt = '%H:%M:%S')

logger = logging.getLogger("communication_node")

# Set logging levels for specific modules
logging.getLogger("asyncua").setLevel(logging.CRITICAL)
logging.getLogger("asyncio").setLevel(logging.WARNING)

# ---------------------------------------------------------------------------- #
# PARAMETERS AND TOPICS FOR CONNECTION WITH MQTT

IP_ADDRESS         = "localhost"       # IP address of the MQTT broker
PORT               = 1883              # Port number for the MQTT broker
POSE_TOPIC         = "turtle/pose"     # Topic for turtle pose messages
CMD_VEL_TOPIC      = "turtle/cmd_vel"  # Topic for turtle velocity commands

# ---------------------------------------------------------------------------- #
# OPC-UA SERVER CLASS

class OPC_UA_Server(threading.Thread):

    def __init__(self):
        """
        Initialize the OPC-UA Server & MQTT Subscriber.

        This constructor performs the following steps:
            1. Calls the parent class constructor.
            2. Creates and initializes the MQTT client.
            3. Creates and initializes the OPC-UA server.
        """
        # STEP 1: Call the parent class constructor ----------------------------

        super().__init__()
        self._stop_event = threading.Event()

        # STEP 2: Create and initialize MQTT Client ----------------------------
        
        # Declare here to avoid executing the on_message callback before
        # initializing the server
        self.server_on = False

        # Create an instance of the MQTT client
        self.client = mqtt.Client("OPC-UA_Server_MQTT_Subscriber")
        self.initialize_mqtt()

        # STEP 3: Create and initialize OPC-UA Server --------------------------

        # Start the OPC-UA server
        self.server = Server()
        self.initialize_server()

        ### end def __init__() ###

    def initialize_mqtt(self):
        """
        Initialize the MQTT client and connect to the broker.
        """
        self.client.on_message = self.on_message

        try:
            # Establish a connection to the MQTT broker
            self.client.connect(IP_ADDRESS, PORT)

            # Log a message indicating successful connection
            logger.info(
                f"Connected to broker (ip: {IP_ADDRESS}, port: {PORT})")

        except KeyboardInterrupt:
            # Log a warning and exit if interrupted by the user
            logger.warning("Closing program due to KeyboardInterrupt")
            sys.exit(1)

        except Exception as err:
            # Log an error message if there is an issue with the connection
            logger.error(f"MQTT connection error: {err}")

            # Log a warning and exit the program
            logger.warning("Closing program due to error")
            sys.exit(1)      
            
        # Subscribe to the relevant topics
        self.client.subscribe(POSE_TOPIC)
        self.client.subscribe(CMD_VEL_TOPIC)

        # Start the MQTT client loop
        self.client.loop_start()

        ### end def initialize_mqtt() ###

    def on_message(self, client, userdata, message):
        """
        Callback for when a message is received from the subscribed topic.
        """        
        if self.server_on:
            logger.info(f"Message recieved from {message.topic}...")

            raw_msg = message.payload.decode()
            # Decode the message payload and load it as a JSON object
            json_msg = json.loads(raw_msg)

            # Update the node variables based on the received message
            if message.topic == POSE_TOPIC:
                # Update Position variable
                self.pose_position_var.write_value(
                    json_msg["position"], ua.VariantType.Double)
                
                # Update Orientation variable
                self.pose_orientation_var.write_value(
                    json_msg["orientation"], ua.VariantType.Double)  
            
                # Update Linear Velocity variable  
                self.pose_linear_velocity_var.write_value(
                    json_msg["linear_velocity"], ua.VariantType.Double)
                
                # Update Angular Velocity variable
                self.pose_angular_velocity_var.write_value(
                    json_msg["angular_velocity"], ua.VariantType.Double)
                
                # Increment the pose message counter
                self.pose_msg_counter_var.write_value(
                    self.pose_msg_counter_var.read_value() + 1
                    , ua.VariantType.Int64)

                logger.debug("pose node variables updated on server")
            
            elif message.topic == CMD_VEL_TOPIC:
                # Update Linear Velocity variable for cmd_vel
                self.cmd_vel_linear_var.write_value(
                    json_msg["linear"], ua.VariantType.Double)
                
                # Update Angular Velocity variable for cmd_vel
                self.cmd_vel_angular_var.write_value(
                    json_msg["angular"], ua.VariantType.Double)
                
                # Increment the cmd_vel message counter
                self.cmd_vel_msg_counter_var.write_value(
                    self.cmd_vel_msg_counter_var.read_value() + 1
                    , ua.VariantType.Int64)

                logger.debug("Value of cmd_vel node variables updated on server")

            else:
                # Handle unexpected topics
                pass
        
        ### end def on_message() ###

    def initialize_server(self):
        """
        Initialize the OPC-UA server.
        """
        # STEP 1: Set the server endpoint --------------------------------------

        self.server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")

        # Create a namespace; useful for organization
        self.uri = "http://localhost/mynamespace" 

        logger.debug("Registering namespace...")
        # Register the namespace
        self.idx = self.server.register_namespace(self.uri) 
        logger.debug(f"Namespace registered with index: {self.idx}")

        # STEP 2: Start the server ---------------------------------------------

        # Log message indicating server start
        logger.info("Starting the server...")

        # Load definitions into the namespace and start the server
        self.server.start()

        # Log message indicating server initialization starts
        logger.info("Initializing the server...")

        # Wait for 30 seconds, but check the stop event every 0.01 seconds
        total_sleep_time = 30
        interval = 0.01
        elapsed_time = 0

        while elapsed_time < total_sleep_time:
            if self._stop_event.is_set():
                logger.info("Stop event set, exiting initialization")
                self.server.stop()
                sys.exit(1)
            
            try:
                sleep(interval)

            except KeyboardInterrupt:
                self._stop_event.set()

            elapsed_time += interval

        # Log message indicating server initialization fisished
        logger.info("Server initialized")

        # STEP 3: Create nodes and variables -----------------------------------

        # Log message indicating node creation starts
        logger.info("Creating new nodes...")

        # Create pose object node and its variables
        logger.debug("Creating pose object node...")
        self.pose_obj = self.server.nodes.objects.add_object(
            self.idx
            , "pose")
        logger.debug("Pose object node created")

        self.pose_msg_counter_var = self.pose_obj.add_variable(
            self.idx
            , "pose_msg_counter"
            , 0
            , ua.VariantType.Int64)
        self.pose_msg_counter_var.set_writable()
        logger.debug("Pose Message Counter variable created and set writable")

        self.pose_position_var = self.pose_obj.add_variable(
            self.idx
            , "position"
            , [0.0, 0.0]
            , ua.VariantType.Double)
        self.pose_position_var.set_writable()
        logger.debug("Position Variable created and set writable")

        self.pose_orientation_var = self.pose_obj.add_variable(
            self.idx
            , "orientation"
            , 0.0
            , ua.VariantType.Double)
        self.pose_orientation_var.set_writable()
        logger.debug("Orientation Variable created and set writable")

        self.pose_linear_velocity_var = self.pose_obj.add_variable(
            self.idx
            , "linear_velocity"
            , 0.0
            , ua.VariantType.Double)
        self.pose_linear_velocity_var.set_writable()
        logger.debug("Linear Velocity created and set writable")
        
        self.pose_angular_velocity_var = self.pose_obj.add_variable(
            self.idx
            , "angular_velocity"
            , 0.0
            , ua.VariantType.Double) 
        self.pose_angular_velocity_var.set_writable()
        logger.debug("Angular Velocity created and set writable")

         # Create cmd_vel object node and its variables
        logger.debug("Creating cmd_vel object node...")
        self.cmd_vel_obj = self.server.nodes.objects.add_object(
            self.idx
            , "cmd_vel")
        logger.debug("cmd_vel object node created")

        self.cmd_vel_msg_counter_var = self.cmd_vel_obj.add_variable(
            self.idx
            , "cmd_vel_msg_counter"
            , 0
            , ua.VariantType.Int64)
        self.cmd_vel_msg_counter_var.set_writable()
        logger.debug("cmd_vel Msg Counter variable created and set writable")

        self.cmd_vel_linear_var = self.cmd_vel_obj.add_variable(
            self.idx
            , "linear"
            , [0.0, 0.0, 0.0]
            , ua.VariantType.Double)
        self.cmd_vel_linear_var.set_writable()
        logger.debug("Linear created and set writable")
        
        self.cmd_vel_angular_var = self.cmd_vel_obj.add_variable(
            self.idx
            , "angular"
            , [0.0, 0.0, 0.0]
            , ua.VariantType.Double)
        self.cmd_vel_angular_var.set_writable()
        logger.debug("Angular created and set writable")

        # Log message indicating node creation
        logger.info("Nodes created")

        # Indicate that the server is active
        self.server_on = True
        
        ### end def initialize_server() ###
    
    def run(self):
        """
        Run the main loop of the server.
        """
        while not self._stop_event.is_set():
            # Sleep briefly to prevent high CPU usage
            sleep(0.001)

        logger.info("Closing server...")

        # Disconnect the MQTT client
        self.client.disconnect()

        # Stop the OPC-UA server
        self.server.stop()

        logger.info("Program closed without errors")

        ### end def run() ###

# ---------------------------------------------------------------------------- #
# # SCRIPT ENTRY POINT

if __name__ == '__main__':
    
    # ------------------------------------------------------------------------ #
    # CREATE OPC-UA SERVER

    server = OPC_UA_Server()

    # ------------------------------------------------------------------------ #
    # START OPC-UA SERVER
    
    server.start()

    # ------------------------------------------------------------------------ #
    # WAIT UNTIL FINISHES
    
    try:
        # Keep the main thread alive until the stop event is set
        while not server._stop_event.is_set():
            sleep(0.001)

    except KeyboardInterrupt:
        # Set the stop event if a keyboard interrupt is detected
        server._stop_event.set()
    
    # Wait for the server thread to finish
    server.join()

# end of file #
