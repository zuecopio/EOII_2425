"""
@file     communication_node.py

@author   Marcos Belda Martinez' <mbelmar@etsinf.upv.es>
@date     January, 2025
@section  EOII-GIIROB
@brief    Implements an MQTT subscriber as a communication bridge between
          ROS 2 and an MQTT broker, subscribing to turtle pose and command
          velocity topics.
"""

# ---------------------------------------------------------------------------- #
# NEEDED IMPORTS

import json                          # For handling JSON data
import logging                       # For logging messages
import sys                           # For using exit() function
from time import sleep, time         # For sleep function

import paho.mqtt.client as mqtt      # For MQTT communication
import rclpy                         # ROS 2 client library
import rclpy.logging
from rclpy.node import Node          # ROS 2 Node class

from turtlesim.msg import Pose       # ROS 2 message type for turtle position
from geometry_msgs.msg import Twist  # ROS 2 message type for velocity

# ---------------------------------------------------------------------------- #
# LOGGER CONFIGURATION

# Basic logger configuration
logging.basicConfig(
    level = logging.INFO
    , format = '%(asctime)s - %(name)s - %(levelname)s'
               ' - %(funcName)s - %(message)s'
    , datefmt = '%H:%M:%S')

logger = logging.getLogger("communication_node")

# Set logging levels for specific modules
# TODO: If needed

# ---------------------------------------------------------------------------- #
# PARAMETERS AND TOPICS FOR CONNECTION WITH MQTT

IP_ADDRESS         = "192.168.1.145"   # IP address of the MQTT broker
PORT               = 1883              # Port number for the MQTT broker
MQTT_POSE_TOPIC    = "turtle/pose"     # Topic for turtle pose messages
MQTT_CMD_VEL_TOPIC = "turtle/cmd_vel"  # Topic for turtle velocity commands

# ---------------------------------------------------------------------------- #
# TOPICS FOR CONNECTION WITH ROS2

ROS2_POSE_TOPIC    = "turtle1/pose"    # Topic for turtle pose messages
ROS2_CMD_VEL_TOPIC = "turtle1/cmd_vel" # Topic for turtle velocity commands

# ---------------------------------------------------------------------------- #
# COMMUNICATION BRIDGE NODE CLASS

class CommunicationBridge(Node):

    def __init__(self):
        """
        Initialize the CommunicationBridge node.
        """
        # STEP 1: Call the parent class constructor ----------------------------

        super().__init__("communication_bridge_node")

        # STEP 2: Create and initialize MQTT Client ----------------------------

        # Create an instance of the MQTT client
        self.publisher = mqtt.Client("communication_bridge_node")
        self.initialize_mqtt() 

        # STEP 3: Initialize the ROS2 node -------------------------------------
        
        self.initialize_node()

        ### end def __init__() ###

    def initialize_mqtt(self):
        """
        Initialize the MQTT client and connect to the broker.
        """
        try:
            # Establish a connection to the MQTT broker
            self.publisher.connect(IP_ADDRESS, PORT)

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
        self.publisher.subscribe(MQTT_POSE_TOPIC)
        self.publisher.subscribe(MQTT_CMD_VEL_TOPIC)

        # Publication times and intervals
        self.pose_last_time       = 0.0  # Last pose publication time
        self.cmd_vel_last_time    = 0.0  # Last cmd_vel publication time
        self.pose_pub_interval    = 0.2  # Pose publication interval (sec)
        self.cmd_vel_pub_interval = 0.2  # cmd_vel publication interval (sec)

        # Start the MQTT client loop
        self.publisher.loop_start()

        ### end def initialize_mqtt() ###

    def initialize_node(self):
        """
        Initialize the ROS2 node by creating subscriptions to relevant topics.
        """
        # Create subscription to "turtle1/pose" topic
        self.pose_subs = self.create_subscription(
            Pose
            , ROS2_POSE_TOPIC
            , self.pose_callback
            , 10)
        logger.info(f"Subscription to '{ROS2_POSE_TOPIC}' topic created")

        # Create subscription to "turtle1/cmd_vel" topic
        self.cmd_vel_subs = self.create_subscription(
            Twist
            , ROS2_CMD_VEL_TOPIC
            , self.cmd_vel_callback
            , 10)
        logger.info(f"Subscription to '{ROS2_CMD_VEL_TOPIC}' topic created")
        
        ### end def initialize_node() ###

    def pose_callback(self, msg):
        """
        Callback function for the "turtle1/pose" topic.
        """
        currentTime = time()

        # if currentTime - self.pose_last_time >= self.pose_pub_interval:
        if True:
            # Update the last publication time
            self.pose_last_time = currentTime

            # Generate JSON message with pose data
            pose_data = {
                "position": [msg.x, msg.y],
                "orientation": msg.theta,
                "linear_velocity": msg.linear_velocity,
                "angular_velocity": msg.angular_velocity
            }
            
            try:
                pose_msg = json.dumps(pose_data)

                # Publish the message to the corresponding MQTT topic
                self.publisher.publish(MQTT_POSE_TOPIC, pose_msg)

                # Log the published message
                logger.info(
                    f"New message sent via MQTT to '{MQTT_POSE_TOPIC}'")
                logger.debug(
                    f"Message content: {pose_msg}")
                
            except Exception as err:
                # Log an error if the message fails to publish
                logger.error(
                    f"Failed to publish pose message: {err}")

        ### end def pose_callback() ###

    def cmd_vel_callback(self, msg):
        """
        Callback function for the "turtle1/cmd_vel" topic.
        """
        currentTime = time()

        # if currentTime - self.cmd_vel_last_time >= self.cmd_vel_pub_interval:
        if True:
            # Update the last publication time
            self.cmd_vel_last_time = currentTime

            # Generate JSON message with cmd_vel data
            cmd_vel_data = {
                "linear": [msg.linear.x, msg.linear.y, msg.linear.z],
                "angular": [msg.angular.x, msg.angular.y, msg.angular.z]
            }

            try:
                cmd_vel_msg = json.dumps(cmd_vel_data)
                 
                # Publish the message to the corresponding MQTT topic
                self.publisher.publish(MQTT_CMD_VEL_TOPIC, cmd_vel_msg)

                # Log the published message
                logger.info(
                    f"New message sent via MQTT to '{MQTT_CMD_VEL_TOPIC}'")
                logger.debug(
                    f"Message content: {cmd_vel_msg}")
                
            except Exception as err:
                # Log an error if the message fails to publish
                logger.error(
                    f"Failed to publish cmd_vel message: {err}")

        ### end def cmd_vel_callback() ###

# ---------------------------------------------------------------------------- #
# MAIN FUNCTION DEFINE

def main(args = None):
    """
    Initialize the ROS 2 Python client library, create the CommunicationBridge
    node, and keep it active until the user interrupts the program with
    Ctrl + C.
    """
    # STEP 1: Initialize rclpy -------------------------------------------------

    rclpy.init(args = args)

    # STEP 2: Create an instance of the node and spin it -----------------------

    communication_bridge = CommunicationBridge()

    # Keep the node active until the user interrupts the program with Ctrl + C
    try:
        rclpy.spin(communication_bridge)

        # Log message before shutting down
        logger.info("Closing program without errors")

    except KeyboardInterrupt:
        # Log a warning if interrupted by the user
        logger.warning("Closing program due to KeyboardInterrupt")
        pass

    except Exception as err:
        # Log any unexpected errors
        logger.error(f"Unexpected error: {err}")

    # STEP 3: Properly shut down the program -----------------------------------

    # Disconnect MQTT and destroy the node
    communication_bridge.publisher.disconnect()
    communication_bridge.destroy_node()

    # Check if the context is already shut down before calling rclpy.shutdown()
    if rclpy.ok():
        rclpy.shutdown()

    ### end def main() ###

# ---------------------------------------------------------------------------- #
# SCRIPT ENTRY POINT

if __name__ == '__main__':
    main()

# end of file #
