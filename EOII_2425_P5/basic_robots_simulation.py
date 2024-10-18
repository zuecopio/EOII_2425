"""
@file     basic_robots_simulation.py

@author   Marcos Belda Martinez <mbelmar@etsinf.upv.es>
@date     October, 2024
@section  EOII-GIIROB
@brief    Basic Robots Simulation.
"""

# ---------------------------------------------------------------------------- #
# NEEDED IMPORTS

import json
import threading
import time
import tkinter as tk
import paho.mqtt.client as mqtt

# ---------------------------------------------------------------------------- #
# PARAMETERS AND TOPICS FOR CONNECTION WITH MQTT

BROKER   = 'broker.emqx.io'
PORT     =  1883
USERNAME = 'emqx'
PASSWORD = 'public'

TOPICS = {
    "Robot1": "Robot1/target_pos",
    "Robot2": "Robot2/target_pos",
    "Robot3": "Robot3/target_pos"
}

target_positions = {
    "Robot1": {"x": 15, "y":  5},
    "Robot2": {"x": 20, "y": 30},
    "Robot3": {"x": 40, "y": 40}
}

# ---------------------------------------------------------------------------- #
# GLOBAL VARIABLES

WINDOW_SIZE = 50
ROBOT_SIZE  = 10

# ---------------------------------------------------------------------------- #
# ROBOT OBJECT CLASS

class Robot(threading.Thread):

    def __init__(self, canvas, robot_id, name, color, start_pos):
        """
        Initializes a robot attributes.
        """
        super().__init__()
        self.canvas = canvas
        self.robot_id = robot_id
        self.name = name
        self.color = color
        self.current_pos = start_pos
        self.target_pos = None # Assigned through the corresponding topic
        self.robot_size = ROBOT_SIZE
        self._stop_event = threading.Event()

        # Configuración subscriptor MQTT
        self.client = mqtt.Client(self.name)
        self.client.connect(BROKER, PORT, 60)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print(f"{self.name} successfully connected")
        # Subscribe to the corresponding topic to receive the objective
        self.client.subscribe(TOPICS[self.name])
        
    def on_message(self, client, userdata, message):
        objetive = json.loads(message.payload.decode())
        self.target_pos = [objetive["x"], objetive["y"]]
        print(f"Target of {self.name}: {self.target_pos}")
        
    def run(self):
        """
        Defines the logic of the robot's movement from its current position
        to its target. This method runs on a separate thread for each robot.
        """
        while self.target_pos == None:
            time.sleep(0.1)

        print(f"{self.name} ({self.color}) - Starting in position {self.current_pos} with target {self.target_pos}")
        
        # The robot is represented as a circle on the canvas
        self.robot_shape = self.canvas.create_oval(
            self.current_pos[0] * self.robot_size, self.current_pos[1] * self.robot_size, 
            (self.current_pos[0] + 1) *  self.robot_size, (self.current_pos[1] + 1) * self.robot_size,
            fill=self.color
        )
        # represent the target
        self.target_shape = self.canvas.create_rectangle(
            self.target_pos[0] * self.robot_size, self.target_pos[1] * self.robot_size, 
            (self.target_pos[0] + 1) *  self.robot_size, (self.target_pos[1] + 1) * self.robot_size,
            fill=self.color)

        while self.current_pos != self.target_pos and not self._stop_event.is_set():
            self.move_towards_target()
            self.update_position_on_canvas()
            time.sleep(0.5)  # Pause to simulate movement
            
        if not self._stop_event.is_set():
            print(f"{self.name} ({self.color}) - Has reached the position {self.target_pos}!")

    def move_towards_target(self):
        """
        Moves the robot one step in the direction of the
        target, modifying the coordinates on the X and Y axes.
        """
        # Move on X axis
        if self.current_pos[0] < self.target_pos[0]:
            self.current_pos[0] += 1
        elif self.current_pos[0] > self.target_pos[0]:
            self.current_pos[0] -= 1

        # Move on Y axis
        if self.current_pos[1] < self.target_pos[1]:
            self.current_pos[1] += 1
        elif self.current_pos[1] > self.target_pos[1]:
            self.current_pos[1] -= 1

    def update_position_on_canvas(self):
        """
        Updates the robot position on the canvas.
        """
        self.canvas.coords(
            self.robot_shape,
            self.current_pos[0] * self.robot_size, self.current_pos[1] * self.robot_size,
            (self.current_pos[0] + 1) * self.robot_size, (self.current_pos[1] + 1) * self.robot_size
        )

    def stop(self):
        """
        Stops the robot's movement when called.
        """
        self._stop_event.set()

# ---------------------------------------------------------------------------- #
# ROBOT SIMULATOR APP OBJECT CLASS

class RobotSimulatorApp:
    
    def __init__(self, root):
        """
        Creates the window, canvas, and control buttons.
        """
        self.root = root
        self.root.title("Robots Simulator")

        # Create the canvas where the robots will move
        self.canvas = tk.Canvas(self.root, width=ROBOT_SIZE*WINDOW_SIZE, height=ROBOT_SIZE*WINDOW_SIZE)
        self.canvas.pack()

        # Button to start the simulation
        self.start_button = tk.Button(self.root, text="Start Simulation", command=self.start_simulation)
        self.start_button.pack(pady=10)

        # Create the robots and show their initial position
        self.robots = [
            Robot(self.canvas, 1, "Robot1", "red", [1, 1]),
            Robot(self.canvas, 2, "Robot2", "green", [48, 1]),
            Robot(self.canvas, 3, "Robot3", "blue", [1, 48])
        ]
        self.display_initial_positions()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # MQTT publisher configuration
        self.client = mqtt.Client("simulator")
        self.client.connect(BROKER, PORT, 60)  

    def display_initial_positions(self):
        """
        Shows the initial position of the robots
        on the canvas, without them moving yet.
        """
        # Draw the robots in their initial position (without moving yet)
        for robot in self.robots:
            robot.robot_shape = self.canvas.create_oval(
                robot.current_pos[0] * robot.robot_size, robot.current_pos[1] * robot.robot_size,
                (robot.current_pos[0] + 1) * robot.robot_size, (robot.current_pos[1] + 1) * robot.robot_size,
                fill=robot.color
            )

    def publish_objetive(self, robot_name, target_pos):
        """
        Publish robot targets in JSON format at the start of the simulation.
        """
        self.client.publish(TOPICS[robot_name], json.dumps(target_pos))

    def start_simulation(self):
        """
        Starts the simulation, removing the initial static
        shapes and launching the robot threads
        """
        # Publish the objectives in the broker
        for robot_name, target_pos in target_positions.items():
            self.publish_objetive(robot_name, target_pos)
        # Remove initial shapes from the canvas
        for robot in self.robots:
            self.canvas.delete(robot.robot_shape)
        # Start the robot threads so they start moving
        for robot in self.robots:
            robot.start()
        # Disable the button so that only one simulation can be done
        self.start_button["state"] = "disabled"
    
    def stop_simulation(self):
        """
        Stops all robots if necessary.
        """
        for robot in self.robots:
            robot.stop()

    def on_closing(self):
        """
        Stops the simulation and closes the application window.
        """
        self.stop_simulation()
        self.root.destroy()

# ---------------------------------------------------------------------------- #
# CREATE YHE MAIN WINDOW AND RUN THE SIMULATOR
root = tk.Tk()
app = RobotSimulatorApp(root)
root.mainloop()

# end of file #