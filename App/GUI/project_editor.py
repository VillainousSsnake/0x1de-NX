# /App/GUI/project_editor.py
# Contains code for project editor

# Importing libraries and modules
from PIL import ImageTk
import customtkinter as ctk
import os


# Defining project_editor
def project_editor(app):

    # Setting theme
    ctk.set_appearance_mode(app.settings["current_theme"])

    # Creating root window
    root = ctk.CTk()
    root.title("0x1de-NX | Alpha v0.0.1")
    root.geometry("850x525+200+200")
    root.wm_iconbitmap()
    root.iconphoto(
        False,
        ImageTk.PhotoImage(file=os.path.join(os.getcwd(), "App", "Image", "0x1de.ico"))
    )

    # Defining on_close function
    def on_close():
        root.destroy()
        app.returnStatement = "exit"

    # Assigning the buttons on the tkinter window top bar
    root.protocol("WM_DELETE_WINDOW", on_close)

    # TODO: Add code here

    # Root mainloop (End of function)
    root.mainloop()
