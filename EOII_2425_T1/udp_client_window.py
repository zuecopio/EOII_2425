"""
@file     udp_client_window.py

@author   Marcos Belda Martinez' <mbelmar@etsinf.upv.es>
@date     October, 2024
@section  EOII-GIIROB
@brief    UDP Client Window implementation using tkinter.
"""

# ---------------------------------------------------------------------------- #
# NEEDED IMPORTS

import ipaddress
from   styles  import *
from   tkinter import messagebox
import tkinter as tk
import udp_client_class as udp_c

# ---------------------------------------------------------------------------- #
# FUNCTIONS

def ip_is_valid(serverIP):
    """
    Function to check if IP value is valid.
    """    
    isValid = False

    if serverIP.lower() == "localhost":
        isValid = True
    
    else:
        try:
            # Try to create an IP address object
            ipaddress.ip_address(serverIP)
            isValid = True
        
        except ValueError:
            pass

    return isValid

    ### end def ip_is_valid() ###

def checkServerAddressEntries():
    """
    Function to check the entries value and to show errors.
    """
    valuesAreValid = False

    # Not highlight serverAddress_button
    serverAddress_button.config(
        highlightbackground = FRAME_BG_COLOR,
        highlightcolor = FRAME_BG_COLOR,
        highlightthickness = 1)

    # Get serverIP_entry value and check if is valid
    serverIP = serverIP_entry.get()
    serverIP_valid = ip_is_valid(serverIP)

    # Get serverPort_entry value and check if is valid
    port = serverPort_entry.get()
    port_valid = ((port.isdigit()) and
                  (int(port) > 1024) and
                  (int(port) < 65535))

    # Case 1: Values are valid -------------------------------------------------

    if (serverIP_valid == True) and (port_valid == True):
        # Update boolean variable
        valuesAreValid = True
        
        # Not highlight entries
        serverIP_entry.config(
            highlightbackground = FRAME_BG_COLOR,
            highlightcolor = FRAME_BG_COLOR,
            highlightthickness = 1)
        
        serverPort_entry.config(
            highlightbackground = FRAME_BG_COLOR,
            highlightcolor = FRAME_BG_COLOR,
            highlightthickness = 1)

    # Case 2: Server IP is not valid -------------------------------------------

    if ((serverIP_valid == False) or (serverIP == "")):
        if serverIP == "":
            # Sends a warning to the user
            messagebox.showerror(
                "Error",
                "Server IP is empty!")
        
        else: # serverIP_valid == False
            # Delete all content to try again
            serverIP_entry.delete(0, tk.END)
            # Set server_IP_address to None
            client.server_IP_address = None
            # Sends a warning to the user
            messagebox.showerror(
                "Error",
                "Invalid Server IP value")
            
        # Highlight IP_entry
        serverIP_entry.config(
            highlightbackground = "RED",
            highlightcolor = "RED",
            highlightthickness = 2)
    
    # Case 3: Server port is not valid -----------------------------------------

    if ((port_valid == False) or (port == "")):
        if port == "":
            # Sends a warning to the user
            messagebox.showerror(
                "Error",
                "Server port is empty!")
        
        else: # (port_valid == False)
            # Delete all content to try again
            serverPort_entry.delete(0, tk.END)
            # Set server_port to None
            client.server_port = None
            # Sends a warning to the user
            messagebox.showerror(
                "Error", 
                ("Invalid Server port value. Port must " +
                 "be a number between 1024 and 65535"))
                    
        # Highlight port_entry
        serverPort_entry.config(
            highlightbackground = "RED",
            highlightcolor = "RED",
            highlightthickness = 2)

    # Check individually the entries to not highlight --------------------------

    if serverIP_valid == True:
        # Not highlight serverIP_entry
        serverIP_entry.config(
            highlightbackground = FRAME_BG_COLOR,
            highlightcolor = FRAME_BG_COLOR,
            highlightthickness = 1)
    
    if port_valid == True:
        # Not highlight serverPort_entry
        serverPort_entry.config(
            highlightbackground = FRAME_BG_COLOR,
            highlightcolor = FRAME_BG_COLOR,
            highlightthickness = 1)

    # Return boolean value of the checking
    return valuesAreValid

    ### def checkEntriesValues() ###

def setServerAddress_clicked(IP_entry, port_entry):
    """
    Function to be executed when "Set server address" button is pressed.
    """
    if checkServerAddressEntries() == True:
        client.setServerAddress(
            new_IP_address = str(IP_entry.get()),
            new_port = int(port_entry.get()))

    ### end def setServerAddress_clicked() ###

def checkMessageEntry():
    """
    Function to check the entry values and to show errors.
    """
    valuesAreValid = False

    # Get message_entry value
    message = message_entry.get()

    # Case 1: Server IP and Server port has not been set -----------------------

    if ((client.server_IP_address == None) or (client.server_port == None)):
        # Sends a warning to the user
        messagebox.showerror(
            "Error",
            "You must set server address before send!")
        
        # highlight serverAddress_button
        serverAddress_button.config(
            highlightbackground = "RED",
            highlightcolor = "RED",
            highlightthickness = 2)

    # Case 2: Message is empty -------------------------------------------------

    elif message == "":
        # Sends a warning to the user
        messagebox.showerror(
            "Error",
            "Message is empty!")
    
    # Case 3: Message is valid -------------------------------------------------

    elif ((message != "") and (len(message.encode()) < 4096)):
        valuesAreValid = True

    # Case 4: Message is too long ----------------------------------------------

    else:
        # Sends a warning to the user
        messagebox.showerror(
            "Error",
            "The message exceeds buffer size")
    
    # Return boolean value of the checking
    return valuesAreValid

    ### def checkMessageEntry() end ###

def sendMessage_clicked(msg_entry):
    """
    Function to be executed when "Send message" button is pressed.
    """
    message = msg_entry.get()

    if checkMessageEntry() == True:
        message_button.config(
                bg = "LIGHT GRAY",
                state = "disabled",
                text = "Sending...")

        window.update() # Ask for repaint function 
        
        # Send message to server
        client.sendMessage(str(message))

    ### end def sendMessage_clicked() ###

# ---------------------------------------------------------------------------- #
# TKINTER

if __name__ == "__main__":
     
    #-----------------------------------------------------#
    #     MAIN WINDOW                                     #
    #-----------------------------------------------------#
    
    # Create the main window
    window = tk.Tk()
    window.title("Send messages")
    window.config(bg = BACKGROUND_COLOR)

    #-----------------------------------------------------#
    #     UDP CLIENT TITLE                                #
    #-----------------------------------------------------#

    # Create a label with background and text color
    tk.Label(
        window,
        fg   = LABEL_FG_COLOR,
        font = TITLE_FONT,
        text = "UDP CLIENT INTERFACE"
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
        sticky = "EW")

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
        command = lambda: setServerAddress_clicked(
            serverIP_entry, 
            serverPort_entry),
        fg      = BUTTON_FG_COLOR,
        text    = "Set server address")

    serverAddress_button.grid(
        column     =  0,
        columnspan =  2,
        row        =  2,
        pady       = 10)
   
    #-----------------------------------------------------#
    #     FRAME FOR SENDING MESSAGES                      #
    #-----------------------------------------------------#

    # Informative label of the section
    tk.Label(
        window,
        bg   = BACKGROUND_COLOR,
        fg   = SECTION_FG_COLOR,
        font = SECTION_FONT,
        text = "\nSend message to server"
        ).grid(
            row    =  1,
            column =  1,
            padx   = 15,
            sticky = 'W')

    # Frame for Message, InfoMessage and Send message
    message_frame = tk.Frame(
        window,
        bg = FRAME_BG_COLOR,
        borderwidth = 2,
        relief = "groove")

    message_frame.grid(
        row    =  2,
        column =  1,
        padx   = 15,
        pady   =  5,
        sticky = "EW")

    # Label and entry for Message
    tk.Label(
        message_frame,
        bg   = FRAME_BG_COLOR,
        fg   = LABEL_FG_COLOR,
        font = TEXT_FONT,
        text = "Message:",
        ).grid(
            column = 0,
            row    = 0,
            sticky = 'E')
    
    message_entry = tk.Entry(
        message_frame,
        bg    = ENTRY_BG_COLOR,
        fg    = ENTRY_FG_COLOR,
        width = 30)

    message_entry.grid(
        column = 1,
        row    = 0,
        sticky = 'W')

    # Frame for InfoMessage
    infoMessage_frame = tk.Frame(
        message_frame,
        bg   = FRAME_BG_COLOR,
        pady = 2)

    infoMessage_frame.grid(
        column = 1,
        row    = 1,
        sticky = 'E')

    # Label for the asterisk in red and bold
    tk.Label(
        infoMessage_frame,
        bg   = FRAME_BG_COLOR,
        fg   = "RED",
        font = ("", 10, "bold"),
        text = "*"
        ).grid(
            column = 0,
            row    = 1,
            sticky = 'E')

    # Label for the rest of the text in gray
    buffer_label = tk.Label(
        infoMessage_frame,
        bg   = FRAME_BG_COLOR,
        fg   = "GRAY",
        font = TEXT_FONT,
        text = "(max data buffer size: 4096)")
    
    buffer_label.grid(
        column = 1,
        row    = 1,
        sticky = 'W')

    # Button to send message
    message_button = tk.Button(
        message_frame,
        bg      = BUTTON_BG_COLOR,
        command = lambda: sendMessage_clicked(message_entry),
        fg      = BUTTON_FG_COLOR,
        text    = "Send message")

    message_button.grid(
        row    =  2,
        column =  1,
        padx   =  8,
        pady   = 10,
        sticky = 'E')

    #-----------------------------------------------------#
    #     FRAME TO SHOW POSSIBLE COMMANDS                 #
    #-----------------------------------------------------#

    # Informative label of the section
    tk.Label(
        window,
        text = "\nSpecial messages for server",
        fg = SECTION_FG_COLOR,
        bg = BACKGROUND_COLOR,
        font = SECTION_FONT
        ).grid(
            column     =  0,
            columnspan =  2,
            padx       = 15,
            row        =  3,
            sticky     = 'W')

    # Frame for commandInfo
    commandInfo_frame = tk.Frame(
        window,
        bg = FRAME_BG_COLOR,
        borderwidth = 2,
        relief = "groove")

    commandInfo_frame.grid(
        column     =  0,
        columnspan =  2,
        padx       = 15,
        pady       =  5,
        row        =  4,
        sticky     = 'EW')

    tk.Label(
        commandInfo_frame,
        bg   = FRAME_BG_COLOR,
        fg   = LABEL_FG_COLOR,
        font = TEXT_BOLD_FONT,
        text = '\n > "Time"'
        ).grid(
            column = 0,
            row = 0,
            sticky = 'W')
    
    tk.Label(
        commandInfo_frame,
        bg   = FRAME_BG_COLOR,
        fg   = LABEL_FG_COLOR,
        font = TEXT_FONT,
        text = "       The server will answer with its" + 
               " current time, e.g.: [18:01:07]\n",
        ).grid(
            column = 0,
            row    = 1,
            sticky = 'W')
    
    tk.Label(
        commandInfo_frame,
        bg   = FRAME_BG_COLOR,
        fg   = LABEL_FG_COLOR,
        font = TEXT_BOLD_FONT,
        text = ' > "Request serialized message"'
        ).grid(
            column = 0,
            row    = 2,
            sticky = 'W')
    
    tk.Label(
        commandInfo_frame,
        bg   = FRAME_BG_COLOR,
        fg   = LABEL_FG_COLOR,
        font = TEXT_FONT,
        text = "       Server will send back an array of values\n"
        ).grid(
            column = 0,
            row    = 3,
            sticky = 'W')
    
    tk.Label(
        commandInfo_frame,
        bg   = FRAME_BG_COLOR,
        fg   = LABEL_FG_COLOR,
        font = TEXT_BOLD_FONT,
        text = ' > "Request JSON serialized message"'
        ).grid(
            column = 0,
            row    = 4,
            sticky = 'W')
    
    tk.Label(
        commandInfo_frame,
        bg   = FRAME_BG_COLOR,
        fg   = LABEL_FG_COLOR,
        font = TEXT_FONT,
        text = "       Server will send back a JSON document\n"
        ).grid(
            column = 0,
            row    = 5,
            sticky = 'W')
    
    tk.Label(
        commandInfo_frame,
        bg   = FRAME_BG_COLOR,
        fg   = LABEL_FG_COLOR,
        font = TEXT_BOLD_FONT,
        text = ' > "End"'
        ).grid(
            column = 0,
            row    = 6,
            sticky = 'W')
    
    tk.Label(
        commandInfo_frame,
        bg   = FRAME_BG_COLOR,
        fg   = LABEL_FG_COLOR,
        font = TEXT_FONT,
        text = "       Closes server and client\n"
        ).grid(
            column = 0,
            row    = 7,
            sticky = 'w')

    #-----------------------------------------------------#
    #     FRAME FOR THE ARRIVAL OF MESSAGES AND WARNINGS  #
    #-----------------------------------------------------#

    # Informative label of the section
    tk.Label(
        window,
        bg   = BACKGROUND_COLOR,
        fg   = SECTION_FG_COLOR,
        font = SECTION_FONT,
        text = "\nServer messages"
        ).grid(
            column     = 0,
            columnspan = 2,
            padx       = 15,
            row        = 5,
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
        row        = 6,
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
    # CREATE UDP CLIENT

    client = udp_c.udpClient(message_button, output_text, window)

    # ------------------------------------------------------------------------ #
    # START UDP CLIENT

    client.start()

    # ------------------------------------------------------------------------ #
    # WINDOW LOOP START

    # Display the window
    window.mainloop()

    # ------------------------------------------------------------------------ #
    # WAIT UNTIL CLIENT FINISHES

    client.closeClient()
    client.join()

# end of file #
