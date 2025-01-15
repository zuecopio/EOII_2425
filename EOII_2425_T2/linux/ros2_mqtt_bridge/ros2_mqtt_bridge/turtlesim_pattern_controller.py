"""
@file     turtlesim_pattern_controller.py

@author   Marcos Belda Martinez' <mbelmar@etsinf.upv.es>
@date     January, 2025
@section  EOII-GIIROB
@brief    This script creates a ROS2 node that publishes velocity commands to
          make the turtle in the turtlesim simulation draw a specific pattern.
"""

# ---------------------------------------------------------------------------- #
# NEEDED IMPORTS

import logging                       # For logging messages
from math import sin                 # For sin function

import rclpy                         # ROS 2 client library
import rclpy.logging
from rclpy.node import Node          # ROS 2 Node class

from geometry_msgs.msg import Twist  # ROS 2 message type for velocity

# ---------------------------------------------------------------------------- #
# LOGGER CONFIGURATION

# Basic logger configuration
logging.basicConfig(
    level = logging.INFO
    , format = '%(asctime)s - %(name)s - %(levelname)s'
               ' - %(funcName)s - %(message)s'
    , datefmt = '%H:%M:%S')

logger = logging.getLogger("turtlesim_pattern_controller")

# Set logging levels for specific modules
# TODO: If needed

# ---------------------------------------------------------------------------- #
# TOPIC FOR CONNECTION WITH ROS2

ROS2_CMD_VEL_TOPIC = "turtle1/cmd_vel" # Topic for turtle velocity commands

# ---------------------------------------------------------------------------- #
# TURTLESIM PATTERN CONTROLLER NODE CLASS

class TurtlesimPatternController(Node):

    def __init__(self):
        """
        Initializes the node and configures the publisher and timer.
        """
        # STEP 1: Call the parent class constructor ----------------------------

        super().__init__("Turtlesim_Pattern_Controller")

        # STEP 2: Initialize the ROS2 node -------------------------------------
        
        self.initialize_node()

        # STEP 3: Initialize the variable for drawing the turtle's pattern -----

        self.variable = 0.0
    
        ### end def __init__() ###
    
    def initialize_node(self):
        """
        Initialize the ROS2 node by creating cmd_vel subscription topic.
        """
        # Create a publisher for the "/turtle1/cmd_vel" topic
        self.cmd_vel_pub = self.create_publisher(
            Twist
            , ROS2_CMD_VEL_TOPIC
            , 10)
        logger.info(f"Subscription to '{ROS2_CMD_VEL_TOPIC}' topic created")

        # Create a timer to call the send_speed method every 0.2 seconds
        self.create_timer(0.2, self.send_speed)

        # Log a message indicating the pattern drawing has started
        logger.info("Drawing a specific pattern with the turtle")
        
        ### end def initialize_node() ###

    def send_speed(self):
        """
        Publishes velocity commands to draw a specific pattern.
        """
        msg = Twist()

        # Set linear and angular velocities based on the pattern
        msg.linear.x = 2.7 + abs(sin(self.variable))
        msg.angular.z = abs(2.0 * sin(self.variable))

        # Publish the velocity command
        self.cmd_vel_pub.publish(msg)

        # Increment the variable for the next pattern calculation
        self.variable += 0.2000768

        # Log the published command
        logger.info(
            f"Command published: linear.x = {msg.linear.x}, "
            f"angular.z = {msg.angular.z}")
    
        ### end def send_speed() ###

# ---------------------------------------------------------------------------- #
# MAIN FUNCTION DEFINITION
    
def main(args=None):
    """
    Initialize the ROS 2 Python client library, create the
    TurtlesimPatternController node, and keep it active until the user
    interrupts the program with Ctrl + C.
    """
    # STEP 1: Initialize rclpy -------------------------------------------------
    
    rclpy.init(args=args)

    # STEP 2: Create an instance of the node and spin it -----------------------

    turtlesim_pattern_controller = TurtlesimPatternController()

    # Keep the node active until the user interrupts the program with Ctrl + C
    try:
        rclpy.spin(turtlesim_pattern_controller)

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

    # Destroy the node after exiting the spin loop
    turtlesim_pattern_controller.destroy_node()

    # Check if the context is already shut down before calling rclpy.shutdown()
    if rclpy.ok():
        rclpy.shutdown()

    ### end def main() ###

# ---------------------------------------------------------------------------- #
# SCRIPT ENTRY POINT
    
if __name__ == '__main__':
    main()
