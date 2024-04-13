# /App/GUI/SubWin/new_project.py
# Contains code for new dialog

# Importing modules, packages and libraries
import App.AppLib.customtkinter as ctk
from functools import partial


# Creating _func class
class _func:
    @staticmethod
    def new_object_type_dropdown_command():
        pass    # TODO: Stub

    @staticmethod
    def object_name_entry_command():
        pass    # TODO: Stub

    @staticmethod
    def close_button_command(window: ctk.CTkToplevel):
        window.destroy()

    @staticmethod
    def create_button_command():
        pass  # TODO: Stub


# Defining new_dialog function
def new_dialog():

    # Setting up the toplevel window
    window = ctk.CTkToplevel()
    window.title("0x1de-NX | New Dialog")
    window.resizable(False, False)
    window.geometry("300x200")

    # Setting focus on the window
    window.focus_set()
    window.grab_set()

    # Creating variables
    object_types_list = [
        "File",
        "Directory",
    ]

    # Creating the frames
    details_frame = ctk.CTkFrame(   # Frame for object details stuff
        master=window,
        height=275,
        fg_color="#242424",
    )
    details_frame.pack(side="top", fill="both")

    # Creating the new window's children
    new_object_type_label = ctk.CTkLabel(   # New object type Label
        master=details_frame,
        text="New Object Type",
        anchor="w",
    )
    new_object_type_label.grid(row=0, column=0, padx=20, pady=10)

    new_object_type_OptionMenu = ctk.CTkOptionMenu(  # Object type OptionMenu
        master=details_frame,
        values=object_types_list,
        command=partial(_func.new_object_type_dropdown_command),
    )
    new_object_type_OptionMenu.grid(row=0, column=1, padx=20, pady=10)

    object_name_label = ctk.CTkLabel(   # Object name Label
        master=details_frame,
        text="Object Name",
        anchor="w",
    )
    object_name_label.grid(row=1, column=0, padx=20, pady=10)

    object_name_entry = ctk.CTkEntry(   # Object name Entry
        master=details_frame,
        placeholder_text="Enter Name Here!",
        command=partial(_func.object_name_entry_command),
    )
    object_name_entry.grid(row=1, column=1, padx=20, pady=10)

    close_button = ctk.CTkButton(  # Close Button
        master=window,
        text="Close",
        command=partial(_func.close_button_command, window),
    )
    close_button.pack(side="left", anchor="s")

    create_button = ctk.CTkButton(  # Create Button
        master=window,
        text="Create",
        command=partial(_func.create_button_command),
    )
    create_button.pack(side="right", anchor="s")


