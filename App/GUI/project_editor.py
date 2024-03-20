# /App/GUI/project_editor.py
# Contains code for project editor

# Importing libraries and modules
from App.AppLib.texture_handler import TextureHandle
import customtkinter as ctk
from PIL import ImageTk
import os


# Defining project_editor
def project_editor(app):

    # Setting theme
    ctk.set_appearance_mode(app.settings["current_theme"])

    # Creating root window
    root = ctk.CTk()
    root.title(
        '0x1de-NX | Alpha v0.0.1 | Editing "'
        + os.path.basename(app.variables["open_project_fp"]) + '"'
    )
    root.geometry("1250x700")
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

    # Creating navigation frame
    navigation_frame = ctk.CTkFrame(
        master=root,
        width=40,
    )
    navigation_frame.pack(
        side="left",
        fill='y',
    )

    # Creating project tree frame
    project_tree_frame = ctk.CTkFrame(
        master=root,
        width=400,
        height=9999999,
    )
    project_tree_frame.pack(
        side='left',
        anchor="nw",
        fill='y',
        padx=1,
    )

    # Creating top navigation frame
    top_nav_frame = ctk.CTkFrame(
        master=root,
        height=40,
    )
    top_nav_frame.pack(
        side="top",
        anchor="e",
        fill='x'
    )

    # Creating editor view frame
    editor_frame = ctk.CTkFrame(
        master=root,
        fg_color="#242424",
        width=9999999,
    )
    editor_frame.pack(fill='both', side='right')

    # Getting the textures and loading them into a list
    button_texture_list = []

    for texture_path in TextureHandle.get_texture_directory():
        print(texture_path)     # TODO: Get rid of print statement and add code

    # Creating and configuring children for navigation frame
    # (the frame for the vertical bar on the left)

    menu_option_btn_001 = ctk.CTkButton(
        master=navigation_frame,
        text="",
        width=0,
    )
    menu_option_btn_001.pack(side='top', fill='x')

    # TODO: Configure and create children for each frame

    # Root mainloop (End of function)
    root.mainloop()
