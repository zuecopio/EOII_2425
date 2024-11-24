"""
@file     exercise_about_robots.py

@author   Marcos Belda Martinez' <mbelmar@etsinf.upv.es>
@date     September, 2024
@section  EOII-GIIROB
@brief    Create three robots, each as an independent thread. The robots have
          an ID, color, current position, and position to reach. The position
          is a coordinate on the x and y axes. The threads should simulate the
          movement of the robots towards their target position and should be
          created as a class that inherits from Thread.
"""

# ---------------------------------------------------------------------------- #
# NECESSARY IMPORTS

import threading  # Import threading module for creating and managing threads

# ---------------------------------------------------------------------------- #
# CREATING ROBOT CLASS

class Robot(threading.Thread):
    
    def __init__(self, id, name, color, start_pos, target_pos):
        """
        Function to initialize robot variables.
        The super() method is used to call the constructor of the parent class.
        """
        super().__init__()    
        # Alse: threading.Thread.__init__(self)
        self.id    = id
        self.name  = name
        self.color = color
        self.start_pos  = start_pos
        self.target_pos = target_pos
        
        ### end def __init__() ###
    
    def go_to_target(self):
        """
        Function to move robot from start_pos to target_pos.
        """
        while self.target_pos != self.start_pos:
            
            if self.start_pos[0] < self.target_pos[0]:
                self.start_pos[0] += 1
            
            if self.start_pos[0] > self.target_pos[0]:
                self.start_pos[0] -= 1
            
            if self.start_pos[1] < self.target_pos[1]:
                self.start_pos[1] += 1
                
            if self.start_pos[1] > self.target_pos[1]:
                self.start_pos[1] -= 1
            
            # Print new pose
            print(f"{self.name} ({self.color}) - New pose {self.start_pos}")
            
        ### end def go_to_target() ###
        
    def run(self):
        """
        This functions runs automatically when the thread is started.
        """
        # 1. Welcome message
        print(f"{self.name} ({self.color}) - Start in pose {self.start_pos} with target {self.target_pos}")
        
        # 2. Robot moves from x to y
        self.go_to_target()
        
        # 3. Goodbye message
        print(f"{self.name} ({self.color}) - Has arrived to {self.target_pos} pose!")
        
        ### end def run() ###

# ---------------------------------------------------------------------------- #
# MAIN FUNCTION

if __name__ == '__main__':
    """
    This bla bla
    """
    # CREATING ROBOT THREADS

    robot1 = Robot(id=1, name="Robot 1", color="White", start_pos=[0, 0], target_pos=[7, 4])
    robot2 = Robot(id=2, name="Robot 2", color="Green", start_pos=[3, 5], target_pos=[1, 2])
    robot3 = Robot(id=3, name="Robot 3", color="Black", start_pos=[6, 2], target_pos=[8, 6])

    # STARTING ROBOT THREADS

    robot1.start()
    robot2.start()
    robot3.start()

    # WAIT UNTIL ALL ROBOTS FINISH

    robot1.join()
    robot2.join()
    robot3.join()

    print("All robots have reached their target positions.")

# end of file #