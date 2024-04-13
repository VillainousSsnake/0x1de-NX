# /App/GUI/SubWin/new_project.py
# Contains code for new dialog

# Importing modules, packages and libraries
import App.AppLib.customtkinter as ctk
from tkinter import messagebox
from functools import partial
import os


# Creating _func class
class _func:
    @staticmethod
    def new_object_type_dropdown_command(value):
        print(value)    # TODO: Stub

    @staticmethod
    def object_name_entry_command(event=None):
        pass    # TODO: Stub

    @staticmethod
    def close_button_command(window: ctk.CTkToplevel):
        window.destroy()

    @staticmethod
    def create_button_command(
            new_object_type_option_menu: ctk.CTkOptionMenu,
            object_name_entry: ctk.CTkEntry,
            current_item,
    ):
        # Getting the object type
        object_type = new_object_type_option_menu.get()

        # Getting the object name
        object_name = object_name_entry.get()

        # Detecting the type and creating the object accordingly
        match object_type:

            case "Directory":       # Directory

                # Getting the base directory
                base_dir = current_item["values"][0]
                if os.path.isfile(base_dir):
                    base_dir = os.path.split(base_dir)[0]

                # Combining the base directory with the new, non-existent directory
                new_dir = os.path.join(base_dir, object_name)

                # Creating the new directory
                os.mkdir(new_dir)

                # Output
                messagebox.showinfo(
                    "Create New | Created New Directory",
                    "Created new directory at \"" + new_dir + "\" successfully!"
                )

                # TODO: Update project_treeview

            case "SARC Archive":    # SARC Archive
                pass  # TODO: Stub

            case "AI Node Binary":  # AI Node Binary
                pass  # TODO: Stub

            case "Binary YAML":     # Binary YAML
                pass  # TODO: Stub


# Defining new_dialog function
def new_dialog(current_item):

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
        "Directory",
        "SARC Archive",
        "Binary YAML",
        "AI Node Binary File",
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
    )
    object_name_entry.bind("<Key>", partial(_func.object_name_entry_command))
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
        command=partial(
            _func.create_button_command,
            new_object_type_OptionMenu,
            object_name_entry,
            current_item,
        ),
    )
    create_button.pack(side="right", anchor="s")


