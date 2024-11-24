"""
@file     threads_processes.py

@author   Marcos Belda Martinez' <mbelmar@etsinf.upv.es>
@date     September, 2024
@section  EOII-GIIROB
@brief    Threads and processes in Python.
"""

# ---------------------------------------------------------------------------- #
# NEEDED IMPORTS

import threading        # For creating and managing threads
import time             # For time-related functions, such as sleep
import multiprocessing  # For creating and managing separate processes

# ---------------------------------------------------------------------------- #
# CREATION AND EXECUTION OF 2 THREADS (using threading.Thread)

def print_message_01():
    """
    Definition of print function.
    """
    print(f"Hello, I am thread {threading.current_thread().name}")

    ### end def print_message_01() ###

# Creating threads
thread1 = threading.Thread(target=print_message_01, name="Thread1")
thread2 = threading.Thread(target=print_message_01, name="Thread2")

# Start threads
thread1.start()
thread2.start()

# Wait until threads end
thread1.join()
thread2.join()

# ---------------------------------------------------------------------------- #
# CREATION AND EXECUTION OF 2 THREADS (inheriting from Thread)

# Create a class that inherited from threading.Thread
class MyThread(threading.Thread):

    def run(self):
        """
        This functions runs automatically when the thread is started.
        """
        print(f"Hello, I am thread {self.name}")

        ### end def run() ###

# Create instances from MyThread
thread1 = MyThread(name="Thread1")
thread2 = MyThread(name="Thread2")

# Start threads
thread1.start()
thread2.start()

# Wait until threads end
thread1.join()
thread2.join()

# ---------------------------------------------------------------------------- #
# ANOTHER EXAMPLE OF THREADS (printing with delays)

def print_message_02(message, delay):
    """
    Definition of print function.
    """
    time.sleep(delay)
    print(message)

    ### end def print_message_02() ###

if __name__ == '__main__':
    # Creating threads
    t1 = threading.Thread(target=print_message_02, args=("H1:…ring!", 5))
    t2 = threading.Thread(target=print_message_02, args=("H2:…ring!", 7))
    
    # Start threads
    t1.start()
    t2.start()
    
    # Wait until threads end
    t1.join()
    t2.join()

# ---------------------------------------------------------------------------- #
# EXAMPLE OF PROCESSES (multiprocessing module)

if __name__ == '__main__':
    process1 = multiprocessing.Process(target=print_message_02, args=("Process 1:…ring!", 5))
    process2 = multiprocessing.Process(target=print_message_02, args=("Process 2:…ring!", 7))
    
    # Start processes
    process1.start()
    process2.start()

# end of file #