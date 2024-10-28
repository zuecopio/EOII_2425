"""
@file     udp_server_window.py

@author   Marcos Belda Martinez <mbelmar@etsinf.upv.es>
@date     October, 2024
@section  EOII-GIIROB
@brief    UDP Server Window implementation using tkinter.
"""

# ---------------------------------------------------------------------------- #
# NEEDED IMPORTS

from tkinter import messagebox
import tkinter as tk
from styles import *
import udp_server_class as udp_s

# ---------------------------------------------------------------------------- #
# FUNCTIONS

def button_clicked():
    """
    Function to be executed when the serverAddress_button is pressed.
    """
    value = serverPort_entry.get()

    if ((value.isdigit()) and (int(value) > 1024) and (int(value) < 65535)):
        
        # Set UDP Server port
        server.setServerPort(new_port = int(value))

        # Start UDP Server thread
        server.start()
        
        # Disable serverPort_entry
        serverPort_entry.config(
            highlightbackground = FRAME_BG_COLOR,
            highlightcolor = FRAME_BG_COLOR,
            highlightthickness = 1,
            state = "disabled")
        
        # Disable serverAddress_button
        serverAddress_button.config(bg = "LIGHT GRAY", state = "disabled")

    else:
        # Delete all content to try again
        serverPort_entry.delete(0, tk.END)
        # Sends a warning to the user
        messagebox.showerror(
            "Error",
            ("Invalid Server port value. Port must " +
             "be a number between 1024 and 65535"))
        
        # Highlight serverPort_entry
        serverPort_entry.config(
            highlightbackground = "RED",
            highlightcolor = "RED",
            highlightthickness = 2)

    ### end def button_clicked() ###

def deselect_others(selected):
    """
    Checkbutton lower exclusion function.
    """
    # function to deselect other checkbuttons
    for key in checkbuttons.keys():
        if key != selected:
            checkbuttons[key].set(False)

    ### def deselect_others() end ###

# ---------------------------------------------------------------------------- #
# TKINTER

if __name__ == "__main__":
     
    #-----------------------------------------------------#
    #     MAIN WINDOW                                     #
    #-----------------------------------------------------#
    
    # Create the main window
    window = tk.Tk()
    window.title("Recieve messages")
    window.config(bg = BACKGROUND_COLOR)

    #-----------------------------------------------------#
    #     UDP SERVER TITLE                                #
    #-----------------------------------------------------#

    # Create a label with background and text color
    tk.Label(
        window,
        fg   = LABEL_FG_COLOR,
        font = TITLE_FONT,
        text = "UDP SERVER INTERFACE"
        ).grid(
            column     = 0,
            columnspan = 2,
            row        = 0,
            sticky     = "EW")

    #-----------------------------------------------------#
    #     FRAME TO SET THE SERVER ADDRESS                 #
    #-----------------------------------------------------#

    # Informative label of the section
    tk.Label(
        window,
        bg   = BACKGROUND_COLOR,
        fg   = SECTION_FG_COLOR,
        font = SECTION_FONT,
        text = "\nServer parameters"
        ).grid(
            column =  0,
            row    =  1,
            padx   = 15,
            sticky = 'W')

    # Frame for Server IP, Server Port and Establish Connection
    connection_frame = tk.Frame(
        window,
        bg = FRAME_BG_COLOR,
        borderwidth = 2,
        relief = "groove")
    
    connection_frame.grid(
        column =  0,
        row    =  2, 
        padx   = 15,
        pady   =  5,
        sticky = "NEW")

    # Label and entry for Server IP
    tk.Label(
        connection_frame,
        bg   = FRAME_BG_COLOR,
        fg   = LABEL_FG_COLOR,
        text = "Server IP:"
        ).grid(
            column = 0,
            row    = 0,
            sticky = 'E')
    
    serverIP_entry = tk.Entry(
        connection_frame,
        bg    = ENTRY_BG_COLOR,
        fg    = ENTRY_FG_COLOR,
        width = 10,)

    serverIP_entry.grid(
        column = 1,
        row    = 0,
        sticky = 'W')
    
    serverIP_entry.insert(0, "localhost")
    serverIP_entry.config(state = "disabled")

    # Label and entry for Server port
    tk.Label(
        connection_frame,
        bg   = FRAME_BG_COLOR,
        fg   = LABEL_FG_COLOR,
        text = "Server port:"
        ).grid(
            column = 0,
            row    = 1,
            sticky = 'E')
    
    serverPort_entry = tk.Entry(
        connection_frame,
        bg    = ENTRY_BG_COLOR,
        fg    = ENTRY_FG_COLOR,
        width = 10)
    
    serverPort_entry.grid(
        column = 1,
        row    = 1,
        sticky = 'W')

    # Button to establish connection
    serverAddress_button = tk.Button(
        connection_frame,
        bg      = BUTTON_BG_COLOR,
        command = button_clicked,
        fg      = BUTTON_FG_COLOR,
        text    = "Start server in\na new thread")

    serverAddress_button.grid(
        column     =  0,
        columnspan =  2,
        row        =  2,
        pady       = 10)

    #-----------------------------------------------------#
    #     FRAME TO CONFIGURE CLIENT OUTPUTS               #
    #-----------------------------------------------------#

    # Informative label of the section
    tk.Label(
        window,
        bg   = BACKGROUND_COLOR,
        fg   = SECTION_FG_COLOR,
        font = SECTION_FONT,
        text = "\nClient messages display mode"
        ).grid(
            column =  1,
            row    =  1,
            padx   = 15,
            sticky = 'W')

    # Frame for display modes
    connection_frame = tk.Frame(
        window,
        bg = FRAME_BG_COLOR,
        borderwidth = 2,
        relief = "groove")
    
    connection_frame.grid(
        column =  1,
        row    =  2, 
        padx   = 15,
        pady   =  5,
        sticky = "NEW")

    ###############################################

    # Create checkbutton variables
    check_uppercase = tk.BooleanVar()
    check_lowercase = tk.BooleanVar()
    check_count     = tk.BooleanVar()

    # Create checkbuttons dictionary
    checkbuttons = {
        "check_uppercase" : check_uppercase,
        "check_lowercase" : check_lowercase,
        "check_count"     : check_count
    }

    # Checkbutton for display message in uppercase
    tk.Checkbutton(
        connection_frame,
        bg       = FRAME_BG_COLOR,
        command = lambda : deselect_others("check_uppercase"),
        fg       = LABEL_FG_COLOR,
        text     = "Display message in uppercase",
        variable = check_uppercase
        ).grid(
            column = 0,
            row    = 0,
            sticky = 'W')

    # Checkbutton for display message in lowercase
    tk.Checkbutton(
        connection_frame,
        bg       = FRAME_BG_COLOR,
        command = lambda : deselect_others("check_lowercase"),
        fg       = LABEL_FG_COLOR,
        text     = "Display message in lowercase",
        variable = check_lowercase
        ).grid(
            column = 0,
            row    = 1,
            sticky = 'W')

    # Checkbutton for counting letters, vowels and consonants
    tk.Checkbutton(
        connection_frame,
        bg       = FRAME_BG_COLOR,
        command = lambda : deselect_others("check_count"),
        fg       = LABEL_FG_COLOR,
        text     = "Counting letters, vowels and consonants",
        variable = check_count
        ).grid(
            column = 0,
            row    = 2,
            sticky = 'W')

    #-----------------------------------------------------#
    #     FRAME FOR THE ARRIVAL OF MESSAGES               #
    #-----------------------------------------------------#

    # Informative label of the section
    tk.Label(
        window,
        bg   = BACKGROUND_COLOR,
        fg   = SECTION_FG_COLOR,
        font = SECTION_FONT,
        text = "\nClient messages"
        ).grid(
            column     = 0,
            columnspan = 2,
            padx       = 15,
            row        = 3,
            sticky     = 'W')
        
    # Frame for Output
    output_frame = tk.Frame(
        window,
        bg = BACKGROUND_COLOR,
        borderwidth = 2,
        relief = "groove")

    output_frame.grid(
        column     = 0,
        columnspan = 2,
        row        = 4,
        padx       = 15,
        pady       = 5,
        sticky     = "EW")

    # Create a text box that accepts multiple lines
    output_text = tk.Text(
        output_frame,
        height = 10,
        width  = 65)

    output_text.grid(
        column     = 0,
        columnspan = 2,
        row        = 0,
        sticky     = "EW")

    # Create the scrollbar and associate it with the text box
    scrollbar = tk.Scrollbar(output_frame)

    scrollbar.grid(
        column = 2,
        row    = 0,
        sticky = "NS")

    output_text.config(yscrollcommand = scrollbar.set)
    scrollbar.config(command = output_text.yview)

    # ------------------------------------------------------------------------ #
    # CREATE UDP SERVER

    server = udp_s.udpServer(checkbuttons,output_text, window)
    
    # ------------------------------------------------------------------------ #
    # START UDP SERVER

    # server.start() # -> The server is started with the button_clicked function.

    # ------------------------------------------------------------------------ #
    # WINDOW LOOP START

    # Display the window
    window.mainloop()

    # ------------------------------------------------------------------------ #
    # WAIT UNTIL SERVER FINISHES

    server.closeClient()

     # Join thread if has been started
    if server.is_alive() == True: 
        server.join()

# end of file #