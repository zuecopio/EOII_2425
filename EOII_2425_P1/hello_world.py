"""
@file     hello_world.py

@author   Marcos Belda Martinez' <mbelmar@etsinf.upv.es>
@date     September, 2024
@section  EOII-GIIROB
@brief    Hello World program.
"""

def print_hello(string):
    """
    Definition of print function.
    """
    print(f'Hello {string}')

    ### end def print_hello() ###

if __name__ == '__main__':
    """
    To determine whether the file is running as a main program or whether it
    is being imported as a module. Thus allowing specific code to be executed
    only in the case that the file is running as a main program.
    """
    print_hello('World')

# end of file #