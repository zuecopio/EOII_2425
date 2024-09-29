"""
@file     classes_inheritance_objects.py

@author   Marcos Belda Martinez <mbelmar@etsinf.upv.es>
@date     September, 2024
@section  EOII-GIIROB
@brief    Classes, Inheritance and Objects in Python.
"""

# ---------------------------------------------------------------------------- #
# CREATING RECTANGLE CLASS

class Rectangle:
    num_of_rectangles = 0 # class variable

    def __init__(self, width, high):
        """
        Definition of initialization function.
        """
        self.width = width
        self.high = high
        Rectangle.num_of_rectangles += 1

        ### end def __init__() ###

    def area(self):
        """
        Calculates the rectangle area.
        """
        return self.width * self.high

        ### end def area() ###

    def perimeter(self):
        """
        Calculates the rectangle perimeter.
        """
        return 2 * (self.width + self.high)

        ### end def perimeter() ###

# ---------------------------------------------------------------------------- #
# CREATING RECTANGLE OBJECTS & PAYING WITH THEM

rectangle_01 = Rectangle(4,5)
rectangle_02 = Rectangle(5,10)
rectangle_03 = Rectangle(10,20)
rectangle_04 = Rectangle(15,30)

print(f'Rectangle 1 width = {rectangle_01.width}      ') # Prints 4
print(f'Rectangle 1 high  = {rectangle_01.high}       ') # Prints 5
print(f'Rectangle 1 area  = {rectangle_01.area()}     ') # Prints 20
print(f'Rectangle 1 area  = {rectangle_01.perimeter()}') # Prints 18

print(f'NO. of Rectangles = {Rectangle.num_of_rectangles} \n') # Prints 4

# ---------------------------------------------------------------------------- #
# CREATING SQUARE CLASS (inherits from the Rectangle class)

class Square(Rectangle):
    
    def __init__(self, side):
        """
        Definition of initialization function.
        The super() method is used to call the constructor of the parent class.
        """
        super().__init__(side, side)
        # Also: Rectangle.__init__(self, side, side)

        ### end def __init__() ###

# ---------------------------------------------------------------------------- #
# CREATING SQUARE OBJECT & PAYING WITH IT

square_01 = Square(4)

print(f'Square 1 width = {square_01.width}      ') # Prints 4
print(f'Square 1 high  = {square_01.high}       ') # Prints 4
print(f'Square 1 area  = {square_01.area()}     ') # Prints 16
print(f'Square 1 area  = {square_01.perimeter()}') # Prints 16

# end of file #