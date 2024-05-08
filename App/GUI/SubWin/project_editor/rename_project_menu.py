# /App/GUI/SubWin/project_editor/rename_project_menu.py
# Contains code for rename project dialog

# Importing modules, packages and libraries
import App.AppLib.customtkinter as ctk
from tkinter import messagebox
from functools import partial
import json
import os


# Creating ButtonFunc class
class ButtonFunc:
    @staticmethod
    def cancel(window):
        window.destroy()

    @staticmethod
    def rename(window, app, root, project_name_entry: ctk.CTkEntry):
        """
            settings = {
                "Project Name": None,
                "IconPath": None,
                "Create romfs folder": True,
                "Create README.txt": True,
            }
        """

        # Asking to continue
        yes_cancel_prompt = messagebox.askokcancel(
            "Rename Project",
            f"Rename project to '{project_name_entry.get()}'"
        )

        # Exiting on prompt being False
        if not yes_cancel_prompt:
            window.destroy()
            return 0

        # Renaming the name in the info.json file
        info_json_path = os.path.join(app.variables["open_project_fp"], "info.json")

        with open(info_json_path, "r") as f_in:
            proj_info = json.load(f_in)

        proj_info["Name"] = project_name_entry.get()

        with open(info_json_path, "w") as f_out:
            json.dump(proj_info, f_out)

        # Renaming directory
        os.rename(
            app.variables["open_project_fp"],
            os.path.join(os.path.split(app.variables["open_project_fp"])[0], project_name_entry.get())
        )

        # Destroying tkinter windows
        app.variables["open_project_fp"] = os.path.join(
            os.path.split(app.variables["open_project_fp"])[0], project_name_entry.get()
        )
        window.destroy()
        root.destroy()


# Defining rename_project_dialog function
def rename_project_menu(root, app):

    # Setting up the toplevel window
    window = ctk.CTkToplevel()
    window.title("0x1de-NX | Rename Project")
    window.resizable(False, False)
    window.geometry("600x300")

    # Setting focus on the window
    window.focus_set()
    window.grab_set()

    # Configuring the menu widgets
    project_name_label = ctk.CTkLabel(
        master=window,
        text="Project Name: ",
    )
    project_name_label.pack(side="top", anchor='w')

    project_name_entry = ctk.CTkEntry(
        master=window,
        placeholder_text="Enter new project name here..."
    )
    project_name_entry.pack(side="top", fill='x')
    project_name_entry.insert(0, os.path.basename(app.variables["open_project_fp"]))

    rename_command = partial(ButtonFunc.rename, window, app, root, project_name_entry)
    rename_button = ctk.CTkButton(
        master=window,
        text="Rename",
        command=rename_command
    )
    rename_button.pack(anchor="se", side="right")

    cancel_command = partial(ButtonFunc.cancel, window)
    cancel_button = ctk.CTkButton(
        master=window,
        text="Cancel",
        command=cancel_command,
    )
    cancel_button.pack(anchor="se", side="left")
