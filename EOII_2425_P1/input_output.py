"""
@file     input_output.py

@author   Marcos Belda Martinez' <mbelmar@etsinf.upv.es>
@date     September, 2024
@section  EOII-GIIROB
@brief    Input and output I/O in Python.
"""

# ---------------------------------------------------------------------------- #
# OUTPUT METHODS

### (part 1) ###

print("Hello World!")

### (part 2) ###

num = 5
print("The number is: " + str(num))

### (part 3) ###

with open("file.txt", "w") as f:
    f.write("Hello World on the file!")

### (part 4) ###

numbers = [1, 2, 3, 4, 5]
with open("numbers.txt", "w") as f:
    for num in numbers:
        f.write(str(num) + "\n")

# ---------------------------------------------------------------------------- #
# INPUT METHODS

### (part 1) ###

name = input("Write your name: ")
print("Hello, " + name + "!")

### (part 2) ###

num = int(input("Write a number: "))
print("The writen number is: " + str(num))

### (part 3) ###

with open("file.txt", "r") as f:
    content = f.read()
    print(content)

# ---------------------------------------------------------------------------- #
# SOME EXAMPLES OF THE f-strings USE

### (part 1) ###

name = "Juan"
print(f"Hello, {name}!") # Output: Hello, Juan!

x, y = 4, 5
print(f"The sum of {x} and {y} is {x + y}.")
# Output: The sum of 4 and 5 is 9.

### (part 2) ###

def to_uppercase(text):
    """
    Function uppercase text.
    """
    return text.upper()

    ### end def to_uppercase() ###

message = "hello world!"
print(f"The message is: {to_uppercase(message)}")
# Output: The message is: HELLO, WORLD

### (part 3) ###

pi = 3.14159265
print(f"The value of pi is approximately {pi:.2f}")
# Output: The value of pi is approximately 3.14

# end of file #