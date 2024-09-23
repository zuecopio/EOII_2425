"""
Thread-based application accessing a shared variable synchronously.
"""

# ---------------------------------------------------------------------------- #
# NEEDED IMPORTS

import threading
import time
import matplotlib.pyplot as plt

from random import random # returns random number betwen 0 and 1

# ---------------------------------------------------------------------------- #
# GLOBAL VARIABLES

# Needed variables for Producer & Consumer
MAX_VALUE = 20
MIN_VALUE = 0
NUM_INC   = 20
NUM_DEC   = 20

# Needed variables for Visualizer
visualize = False
values = []

# ---------------------------------------------------------------------------- #
# CREATING CONTAINER CLASS

class Container():

    def __init__(self):
        """
        Definition of initialization function.
        """
        self.shared_variable = 10 # class variable
        self.monitor = threading.Condition() # synchronization object

        ### end def __init__() ###
    
    def increase(self):
        """
        Increase in one the value of shared_variable
        if its current value is < MAX_VALUE.
        """
        with self.monitor:
            while self.shared_variable > MAX_VALUE:
                self.monitor.wait()
            self.shared_variable += 1
            self.monitor.notify_all()

        ### end def increase() ###
        
    def decrease(self):
        """
        Decreases in one the value of shared_variable
        if its current value is > MIN_VALUE.
        """
        with self.monitor:
            while self.shared_variable < MIN_VALUE:
                self.monitor.wait()
            self.shared_variable -= 1
            self.monitor.notify_all()
        
        ### end def decrease() ###
        
    def read_value(self):
        """
        Returns te value of shared_variable.
        """
        return self.shared_variable
        
        ### end def read_value() ###

# ---------------------------------------------------------------------------- #
# CREATING GRAPHIC CLASS

class Graphic():

    def __init__(self, v):
        """
        Definition of initialization function.
        """
        self.graphic_data = v
        # Graphic configuration
        self.fig = plt.figure()
        self.ax  = self.fig.add_subplot(111)
        self.hl  = plt.plot(self.graphic_data)
        plt.title("Threads process synchronization")
        plt.ylim(MIN_VALUE - 1, MAX_VALUE + 1)
        plt.ylabel("shared_variable value")
        plt.xlim(0, len(v))
        plt.xlabel("time")
        plt.show()

# ---------------------------------------------------------------------------- #
# VISUALIZER TARGET FUNCTION

def visualizer(container):
    """
    Code for Visualizer Thread. 
    """
    while visualize:
        values.append(container.read_value())
        time.sleep(0.1) # value is updated 10 times per second.
    
    ### end def visualizer() ###

# ---------------------------------------------------------------------------- #
# PRODUCER TARGET FUNCTION

def producer(container, num_inc):
    """
    Code for Producer Thread.
    """
    for i in range(num_inc):
        container.increase()
        time.sleep(random())
        
    ### end def producer() ###

# ---------------------------------------------------------------------------- #
# CONSUMER TARGET FUNCTION

def consumer(container, num_dec):
    """
    Code for Consumer Thread.
    """
    for i in range(num_dec):
        container.decrease()
        time.sleep(random())
        
    ### end def consumer() ###

# ---------------------------------------------------------------------------- #
# MAIN

# Create Container object
container = Container()

# Create threads
visualizer_thread = threading.Thread(name='Visualizer',
                                     target=visualizer,
                                     args=(container,)) # <- why the coma is there?

producer_thread = threading.Thread(name='Producer',
                                   target=producer,
                                   args=(container, NUM_INC))

consumer_thread = threading.Thread(name='Consumer',
                                   target=consumer,
                                   args=(container, NUM_DEC))

# Start threads
visualize = True
visualizer_thread.start()
producer_thread.start()
consumer_thread.start()

# Wait until producer & consumer threads end
producer_thread.join()
consumer_thread.join()

# Set visualize to false to stop reading more values
visualize = False

# Wait until visualizer thread end
visualizer_thread.join()

# Plot the graphic with the readed values
my_graphic = Graphic(values)

# end of file #