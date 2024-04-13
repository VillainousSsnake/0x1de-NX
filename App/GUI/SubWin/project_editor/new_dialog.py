# /App/GUI/SubWin/new_project.py
# Contains code for new dialog

# Importing modules, packages and libraries
from App.AppLib.file_handler import FileHandler
import App.AppLib.customtkinter as ctk
from tkinter import messagebox, ttk
from functools import partial
import os


# Creating _func class
class _func:
    @staticmethod
    def update_project_treeview(project_treeview: ttk.Treeview, app):

        # Deleting all the treeview items
        project_treeview.delete(*project_treeview.get_children())

        # Re-inserting all the items into the treeview
        sub_directories_ = [x[0] for x in os.walk(app.variables["open_project_fp"])]
        counter_ = 0
        for folder_path_ in sub_directories_:

            # Creating the item parameter variables
            folder_parent_ = folder_path_.replace(
                os.path.basename(folder_path_), ""
            )[:len(
                folder_path_.replace(os.path.basename(folder_path_), "")
            ) - 1]
            folder_iid_ = folder_path_
            folder_text_ = chr(0x0001F4C1) + " " + os.path.basename(folder_path_)

            if os.path.basename(folder_path_) == "romfs":
                folder_text_ = chr(0x0001F4C1) + " 𝐫𝐨𝐦𝐟𝐬"

            # Making the parent an empty string if it is the first folder
            if counter_ == 0:
                folder_parent_ = ""

            # Creating the folder
            project_treeview.insert(
                parent=folder_parent_,
                index=0,
                iid=folder_iid_,
                text=folder_text_,
                tags=["Directory"],
                values=[folder_path_],
            )

            # Creating all the files in the folder and inserting them into the tree
            for file_name_ in os.listdir(folder_path_):
                file_path_ = folder_path_ + "\\" + file_name_
                if os.path.isfile(file_path_):

                    # Creating the item parameter variables
                    file_parent_ = folder_path_
                    file_iid_ = file_path_
                    file_format_ = FileHandler.get_file_info_from_name(file_name_)["format"]
                    file_icon_ = FileHandler.get_file_info_from_name(file_name_)["icon"]
                    file_text_ = file_icon_ + " " + os.path.basename(file_path_)

                    # Making the parent an empty string if it is the first folder
                    if counter_ == 0:
                        file_parent_ = ""

                    # Creating the file
                    project_treeview.insert(
                        parent=file_parent_,
                        index="end",
                        iid=file_iid_,
                        text=file_text_,
                        tags=["File", file_format_],
                        values=[file_path_],
                    )

            counter_ += 1

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
            project_treeview,
            app, window,
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

                _func.update_project_treeview(project_treeview, app)

            case "SARC Archive":    # SARC Archive
                pass  # TODO: Stub

            case "AI Node Binary":  # AI Node Binary
                pass  # TODO: Stub

            case "Binary YAML":     # Binary YAML
                pass  # TODO: Stub

        # Closing window
        window.destroy()


# Defining new_dialog function
def new_dialog(current_item, project_treeview, app):

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
            project_treeview,
            app, window,
        ),
    )
    create_button.pack(side="right", anchor="s")


