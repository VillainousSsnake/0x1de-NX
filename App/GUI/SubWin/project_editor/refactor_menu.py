# /App/GUI/SubWin/project_editor/refactor_menu.py
# Contains code for refactor dialog

# TODO: Convert code past here to rename a file in the project tree instead of renaming a project

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
        pass    # TODO: Stub


# Defining rename_project_dialog function
def refactor_menu(cur_item, project_treeview, app):

    # Setting up the toplevel window
    window = ctk.CTkToplevel()
    window.title("0x1de-NX | Refactor")
    window.resizable(False, False)
    window.geometry("600x300")

    # Setting focus on the window
    window.focus_set()
    window.grab_set()

    print("Refactoring!")  # TODO: Remove
    print(cur_item)

    object_name = os.path.basename(cur_item['values'][0])
    object_type = cur_item['tags'][0]

    match object_type:

        # In the case where the object is a folder
        case "Directory":

            pass    # TODO: Stub

        # In the case where the object is a file
        case "File":

            pass    # TODO: Stub

        case _:     # Throwing type error
            TypeError("Object is not a Directory or File")
